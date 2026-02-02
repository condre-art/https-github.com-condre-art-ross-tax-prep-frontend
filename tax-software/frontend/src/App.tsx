import React, { useEffect } from 'react';

type Badge = {
  iconUrl?: string | null;
  name: string;
  status?: string;
};

type Certificate = {
  title: string;
  type?: string;
  status?: string;
  expiresAt?: string | null;
  downloadUrl: string;
};

const API_BASE = import.meta.env.VITE_API_BASE || '';

async function loadBadgesAndCertificates(authToken: string | null) {
  if (!authToken) return;

  const badgesRes = await fetch(`${API_BASE}/api/badges`, {
    headers: { Authorization: `Bearer ${authToken}` },
  });
  const certRes = await fetch(`${API_BASE}/api/certificates`, {
    headers: { Authorization: `Bearer ${authToken}` },
  });

  if (badgesRes.status === 401 || certRes.status === 401) {
    localStorage.removeItem('auth_token');
    location.reload();
    return;
  }

  const badges = (await badgesRes.json()) as Badge[];
  const certs = (await certRes.json()) as Certificate[];

  renderBadges(badges);
  renderCertificates2(certs);
}

function renderBadges(badges: Badge[]) {
  const grid = document.getElementById('badges-grid');
  if (!grid) return;

  if (!badges.length) {
    grid.innerHTML = `<p style="color:rgba(255,255,255,0.7)">No badges issued yet.</p>`;
    return;
  }

  grid.innerHTML = badges
    .map(
      (b) => `
    <div style="
      display:flex;align-items:center;gap:10px;
      padding:10px 12px;border:1px solid rgba(255,255,255,0.12);
      border-radius:12px;background:rgba(255,255,255,0.04);
      min-width:220px;">
      <div style="width:34px;height:34px;border-radius:10px;overflow:hidden;background:rgba(0,0,0,0.2);display:flex;align-items:center;justify-content:center;">
        ${b.iconUrl ? `<img src="${b.iconUrl}" style="width:100%;height:100%;object-fit:cover;">` : `<span>🏅</span>`}
      </div>
      <div style="flex:1">
        <div style="font-weight:700">${b.name}</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.65)">Status: ${String(b.status).toUpperCase()}</div>
      </div>
    </div>
  `,
    )
    .join('');
}

function renderCertificates2(certs: Certificate[]) {
  const tbody = document.getElementById('certificates-table-2');
  if (!tbody) return;

  if (!certs.length) {
    tbody.innerHTML = `<tr><td colspan="4" style="color:rgba(255,255,255,0.7)">No certificates issued yet.</td></tr>`;
    return;
  }

  tbody.innerHTML = certs
    .map(
      (c) => `
    <tr>
      <td>
        <strong>${c.title}</strong><br>
        <small style="color:rgba(255,255,255,0.5)">${c.type ?? ''}</small>
      </td>
      <td><span class="cert-status ${c.status}">${String(c.status).toUpperCase()}</span></td>
      <td>${c.expiresAt ? new Date(c.expiresAt).toLocaleDateString() : '—'}</td>
      <td>
        <a class="btn btn-secondary" style="padding:8px 10px;display:inline-block;"
           href="${API_BASE}${c.downloadUrl}"
           target="_blank" rel="noopener noreferrer">
           Download
        </a>
      </td>
    </tr>
  `,
    )
    .join('');
}

function App() {
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    loadBadgesAndCertificates(token);
  }, []);

  return (
    <main className="min-h-screen bg-slate-900 text-white">
      <div className="max-w-5xl mx-auto px-4 py-10 space-y-6">
        <header className="space-y-1">
          <h1 className="text-3xl font-bold">eROS Tax Preparation Platform</h1>
          <p className="text-slate-300">
            Frontend application configured for DIY self-service with IRS MeF integration. Connect to the FastAPI backend
            to continue building features.
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2">
          <section className="p-4 rounded-2xl border border-white/10 bg-white/5">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xl font-semibold">Badges</h2>
              <span className="text-xs text-slate-300">Issued achievements</span>
            </div>
            <div id="badges-grid" className="grid gap-3"></div>
          </section>

          <section className="p-4 rounded-2xl border border-white/10 bg-white/5">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xl font-semibold">Certificates</h2>
              <span className="text-xs text-slate-300">Downloadable credentials</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="text-slate-300">
                  <tr>
                    <th className="py-2 pr-2">Certificate</th>
                    <th className="py-2 pr-2">Status</th>
                    <th className="py-2 pr-2">Expires</th>
                    <th className="py-2">Action</th>
                  </tr>
                </thead>
                <tbody id="certificates-table-2" className="divide-y divide-white/10"></tbody>
              </table>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}

export default App;
