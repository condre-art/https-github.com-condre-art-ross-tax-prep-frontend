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
  renderCertificates(certs);
}

function renderBadges(badges: Badge[]) {
  const grid = document.getElementById('badges-grid');
  if (!grid) return;

  if (!badges.length) {
    grid.innerHTML = `<p class="text-slate-400 text-sm">No badges issued yet.</p>`;
    return;
  }

  grid.innerHTML = badges
    .map(
      (b) => `
      <div class="flex items-center gap-3 p-3 rounded-xl border border-white/10 bg-white/5">
        <div class="w-9 h-9 rounded-lg overflow-hidden bg-black/30 flex items-center justify-center">
          ${
            b.iconUrl
              ? `<img src="${b.iconUrl}" class="w-full h-full object-cover" />`
              : `<span>🏅</span>`
          }
        </div>
        <div class="flex-1">
          <div class="font-semibold">${b.name}</div>
          <div class="text-xs text-slate-400">
            Status: ${(b.status || 'active').toUpperCase()}
          </div>
        </div>
      </div>
    `,
    )
    .join('');
}

function renderCertificates(certs: Certificate[]) {
  const tbody = document.getElementById('certificates-table');
  if (!tbody) return;

  if (!certs.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="4" class="py-4 text-slate-400 text-sm">
          No certificates issued yet.
        </td>
      </tr>`;
    return;
  }

  tbody.innerHTML = certs
    .map(
      (c) => `
      <tr class="border-t border-white/10">
        <td class="py-3 pr-2">
          <strong>${c.title}</strong><br />
          <span class="text-xs text-slate-400">${c.type ?? ''}</span>
        </td>
        <td class="py-3 pr-2 text-sm">
          ${(c.status || 'active').toUpperCase()}
        </td>
        <td class="py-3 pr-2 text-sm">
          ${c.expiresAt ? new Date(c.expiresAt).toLocaleDateString() : '—'}
        </td>
        <td class="py-3">
          <a
            class="inline-block px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-sm"
            href="${API_BASE}${c.downloadUrl}"
            target="_blank"
            rel="noopener noreferrer"
          >
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
          <h1 className="text-3xl font-bold">
            eROS Tax Preparation Platform
          </h1>
          <p className="text-slate-300">
            Secure DIY and professional tax platform with IRS MeF integration.
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2">
          {/* Badges */}
          <section className="p-4 rounded-2xl border border-white/10 bg-white/5">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xl font-semibold">Badges</h2>
              <span className="text-xs text-slate-400">
                Issued achievements
              </span>
            </div>
            <div id="badges-grid" className="grid gap-3" />
          </section>

          {/* Certificates */}
          <section className="p-4 rounded-2xl border border-white/10 bg-white/5">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xl font-semibold">Certificates</h2>
              <span className="text-xs text-slate-400">
                Downloadable credentials
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="text-slate-400">
                  <tr>
                    <th className="py-2 pr-2">Certificate</th>
                    <th className="py-2 pr-2">Status</th>
                    <th className="py-2 pr-2">Expires</th>
                    <th className="py-2">Action</th>
                  </tr>
                </thead>
                <tbody
                  id="certificates-table"
                  className="divide-y divide-white/10"
                />
              </table>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}

export default App;
