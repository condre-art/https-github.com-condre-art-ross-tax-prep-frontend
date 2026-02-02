export const requireActiveLicense = (allowedTypes: string[]) =>
  async (req: any, env: any) => {
    const tenantId = req.tenantId;
    const sql = `
      SELECT *
      FROM licenses
      WHERE tenant_id = ?
        AND status = 'active'
        AND license_type IN (${allowedTypes.map(() => "?").join(",")})
        AND (expires_at IS NULL OR expires_at > datetime('now'))
      ORDER BY datetime(starts_at) DESC
      LIMIT 1
    `;
    const row = await env.DB.prepare(sql).bind(tenantId, ...allowedTypes).first();
    if (!row) throw new Response("License required", { status: 402 });
    return row;
  };
