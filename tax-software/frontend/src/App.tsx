import React from 'react';

function App() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-slate-50 text-slate-900">
      <div className="p-6 rounded-lg shadow bg-white space-y-6 max-w-2xl">
        <h1 className="text-2xl font-semibold mb-2">eROS Tax Preparation Platform</h1>
        <p className="text-sm text-slate-700">
          Frontend application configured for DIY self-service with IRS MeF integration. Connect to the FastAPI backend to continue building features.
        </p>
        <section className="space-y-2">
          <h2 className="text-xl font-semibold">Badges</h2>
          <ul className="list-disc list-inside text-sm text-slate-700">
            <li>IRS Authorized e-File Provider</li>
            <li>Data Privacy & Security Compliant</li>
          </ul>
        </section>
        <section className="space-y-2">
          <h2 className="text-xl font-semibold">Certificates</h2>
          <ul className="list-disc list-inside text-sm text-slate-700">
            <li>Annual Filing Season Program (AFSP) Completion</li>
            <li>Continuing Professional Education (CPE) Verified</li>
          </ul>
        </section>
        <section className="space-y-2">
          <h2 className="text-xl font-semibold">Licenses</h2>
          <ul className="list-disc list-inside text-sm text-slate-700">
            <li>Preparer Tax Identification Number (PTIN) Active</li>
            <li>State Tax Preparation License in Good Standing</li>
          </ul>
        </section>
      </div>
    </main>
  );
}

export default App;
