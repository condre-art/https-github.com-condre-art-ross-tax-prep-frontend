import { Router } from "itty-router";
import { jwtVerify } from "jose";

// Minimal Cloudflare Worker implementing badge/certificate/license routes
export interface Env {
  DB: D1Database;
  SENSITIVE_BUCKET: R2Bucket;

  APP_NAME: string;
  LEGAL_ENTITY: string;
  JWT_ISSUER: string;
  JWT_AUDIENCE: string;

  JWT_SECRET: string;
  PASSWORD_PEPPER: string;
}

type AuthedRequest = Request & {
  user?: { sub: string; role: string; tenantId?: string; email?: string };
  tenantId?: string;
};

const router = Router();

/* =========================
   Utilities
========================= */
const json = (data: any, status = 200) =>
  new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });

const nowIso = () => new Date().toISOString();

function getTenantFromHost(req: Request): string | null {
  // Example: tenant slug from subdomain: {tenant}.yourdomain.com
  const host = req.headers.get("host") || "";
  const parts = host.split(".");
  if (parts.length >= 3) return parts[0];
  return null;
}

async function authRequired(req: AuthedRequest, env: Env) {
  const h = req.headers.get("authorization") || "";
  const token = h.startsWith("Bearer ") ? h.slice(7) : "";
  if (!token) throw new Response("Unauthorized", { status: 401 });

  const secret = new TextEncoder().encode(env.JWT_SECRET);
  const { payload } = await jwtVerify(token, secret, {
    issuer: env.JWT_ISSUER,
    audience: env.JWT_AUDIENCE,
  });

  req.user = {
    sub: String(payload.sub || ""),
    role: String(payload.role || "admin"),
    tenantId: payload.tenantId ? String(payload.tenantId) : undefined,
    email: payload.email ? String(payload.email) : undefined,
  };

  return req.user;
}

function requireRole(...roles: string[]) {
  return async (req: AuthedRequest, env: Env) => {
    const u = req.user || (await authRequired(req, env));
    if (!roles.includes(u.role)) throw new Response("Forbidden", { status: 403 });
    return u;
  };
}

async function resolveTenant(req: AuthedRequest, env: Env) {
  // Priority:
  // 1) token tenantId
  // 2) tenant slug from host
  // 3) fallback single-tenant mode: first tenant
  if (req.user?.tenantId) {
    req.tenantId = req.user.tenantId;
    return req.tenantId;
  }

  const slug = getTenantFromHost(req);
  if (slug) {
    const t = await env.DB.prepare("SELECT id FROM tenants WHERE slug = ? AND status = 'active'")
      .bind(slug)
      .first<{ id: string }>();
    if (t?.id) {
      req.tenantId = t.id;
      return req.tenantId;
    }
  }

  const first = await env.DB.prepare("SELECT id FROM tenants ORDER BY created_at ASC LIMIT 1")
    .first<{ id: string }>();
  if (!first?.id) throw new Response("Tenant not configured", { status: 500 });

  req.tenantId = first.id;
  return req.tenantId;
}

/* =========================
   License gating middleware
========================= */
function requireActiveLicense(allowedTypes: Array<"affiliate" | "reseller" | "enterprise">) {
  return async (req: AuthedRequest, env: Env) => {
    await authRequired(req, env);
    const tenantId = await resolveTenant(req, env);

    const row = await env.DB.prepare(
      `
      SELECT *
      FROM licenses
      WHERE tenant_id = ?
        AND status = 'active'
        AND license_type IN (${allowedTypes.map(() => "?").join(",")})
        AND (expires_at IS NULL OR expires_at > datetime('now'))
      ORDER BY datetime(starts_at) DESC
      LIMIT 1
      `
    )
      .bind(tenantId, ...allowedTypes)
      .first<any>();

    if (!row) throw new Response("License required", { status: 402 });
    return row;
  };
}

/* =========================
   R2 signed URL helper (safe fallback)
========================= */
async function getSignedOrStreamUrl(env: Env, key: string, expiresSeconds = 300): Promise<string | null> {
  // If createSignedUrl exists in your runtime, use it.
  // Otherwise return null and use streaming endpoint.
  const anyBucket: any = env.SENSITIVE_BUCKET as any;
  if (typeof anyBucket.createSignedUrl === "function") {
    // Some runtimes use (key, options). Keep it conservative.
    return await anyBucket.createSignedUrl(key, { expiresIn: expiresSeconds });
  }
  return null;
}

/* =========================
   Routes: Badges
========================= */
router.get(
  "/api/badges",
  authRequired,
  resolveTenant,
  requireActiveLicense(["reseller", "enterprise", "affiliate"]),
  async (req: AuthedRequest, env: Env) => {
    const tenantId = req.tenantId!;
    const { results } = await env.DB.prepare(
      `SELECT id, tenant_id as tenantId, name, icon_url as iconUrl, status, issued_at as issuedAt, expires_at as expiresAt
       FROM badges
       WHERE tenant_id = ?
       ORDER BY display_order ASC, datetime(issued_at) DESC`
    )
      .bind(tenantId)
      .all();

    return json(results);
  }
);

/* =========================
   Routes: Certificates
========================= */
router.get(
  "/api/certificates",
  authRequired,
  resolveTenant,
  requireActiveLicense(["reseller", "enterprise"]),
  async (req: AuthedRequest, env: Env) => {
    const tenantId = req.tenantId!;
    const { results } = await env.DB.prepare(
      `SELECT id, tenant_id as tenantId, title, type, status, issued_at as issuedAt, expires_at as expiresAt
       FROM certificates
       WHERE tenant_id = ?
       ORDER BY datetime(issued_at) DESC`
    )
      .bind(tenantId)
      .all();

    // Attach downloadUrl (stream endpoint is always valid)
    const withUrls = results.map((c: any) => ({
      ...c,
      downloadUrl: `/api/certificates/${c.id}/download`,
    }));

    return json(withUrls);
  }
);

// Download PDF (signed url if available else stream)
router.get(
  "/api/certificates/:certificateId/download",
  authRequired,
  resolveTenant,
  requireActiveLicense(["reseller", "enterprise"]),
  async (req: AuthedRequest, env: Env) => {
    const tenantId = req.tenantId!;
    const certificateId = (req as any).params.certificateId as string;

    const cert = await env.DB.prepare(
      `SELECT id, file_key, title
       FROM certificates
       WHERE id = ? AND tenant_id = ?`
    )
      .bind(certificateId, tenantId)
      .first<any>();

    if (!cert?.file_key) return new Response("Not found", { status: 404 });

    // Try signed URL, else stream
    const signed = await getSignedOrStreamUrl(env, cert.file_key, 300);
    if (signed) {
      return Response.redirect(signed, 302);
    }

    const obj = await env.SENSITIVE_BUCKET.get(cert.file_key);
    if (!obj) return new Response("Not found", { status: 404 });

    const headers = new Headers();
    headers.set("content-type", "application/pdf");
    headers.set("content-disposition", `attachment; filename="${cert.title || "certificate"}.pdf"`);
    headers.set("cache-control", "no-store");

    return new Response(obj.body, { status: 200, headers });
  }
);

/* =========================
   Routes: Licenses
========================= */
router.get(
  "/api/licenses/current",
  authRequired,
  resolveTenant,
  async (req: AuthedRequest, env: Env) => {
    const tenantId = req.tenantId!;
    const license = await env.DB.prepare(
      `SELECT id, tenant_id as tenantId, license_type as licenseType, status, seats,
              starts_at as startsAt, expires_at as expiresAt, meta_json as meta
       FROM licenses
       WHERE tenant_id = ?
       ORDER BY datetime(starts_at) DESC
       LIMIT 1`
    )
      .bind(tenantId)
      .first<any>();

    return json(license || { status: "none" });
  }
);

router.post(
  "/api/licenses/purchase",
  authRequired,
  resolveTenant,
  requireRole("admin", "owner", "reseller"),
  async (req: AuthedRequest, env: Env) => {
    const body = await req.json().catch(() => ({} as any));
    const licenseType = String(body.licenseType || "reseller");
    const seats = Number(body.seats || 1);
    const tenantId = req.tenantId!;
    const startsAt = body.startsAt || nowIso();
    const expiresAt = body.expiresAt || null;
    const meta = body.meta ? JSON.stringify(body.meta) : null;

    await env.DB.prepare(
      `INSERT INTO licenses (tenant_id, license_type, status, seats, starts_at, expires_at, meta_json)
       VALUES (?, ?, 'active', ?, ?, ?, ?)`
    )
      .bind(tenantId, licenseType, seats, startsAt, expiresAt, meta)
      .run();

    return json({ ok: true, licenseType, seats, tenantId, startsAt, expiresAt });
  }
);

router.post(
  "/api/licenses/verify",
  authRequired,
  resolveTenant,
  async (req: AuthedRequest, env: Env) => {
    const tenantId = req.tenantId!;
    const license = await env.DB.prepare(
      `SELECT id, tenant_id as tenantId, license_type as licenseType, status,
              starts_at as startsAt, expires_at as expiresAt
       FROM licenses
       WHERE tenant_id = ?
         AND status = 'active'
       ORDER BY datetime(starts_at) DESC
       LIMIT 1`
    )
      .bind(tenantId)
      .first<any>();

    const now = new Date();
    const valid =
      !!license && (!license.expiresAt || new Date(license.expiresAt) > now) && license.status === "active";

    return json({ valid, license });
  }
);

/* =========================
   Router fallback & export
========================= */
router.all("*", () => new Response("Not Found", { status: 404 }));

export default {
  fetch: (req: AuthedRequest, env: Env, ctx: ExecutionContext) => {
    return router.handle(req, env, ctx);
  },
};

