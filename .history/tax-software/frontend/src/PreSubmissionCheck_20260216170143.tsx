import React, { useState } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE || '';

export default function PreSubmissionCheck() {
  const [form, setForm] = useState({ name: '', ssn: '', refund_amount: '', ein: '', user_id: '' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    const res = await fetch(`${API_BASE}/api/workflow/pre_submission_check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, refund_amount: Number(form.refund_amount) })
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  }

  return (
    <section className="p-4 rounded-2xl border border-white/10 bg-white/5 mt-8">
      <h2 className="text-xl font-semibold mb-2">Pre-Submission Check (EWS 2.0, CADE2, Risk, AI)</h2>
      <form className="grid gap-3 md:grid-cols-2" onSubmit={handleSubmit}>
        <input className="p-2 rounded bg-slate-800 text-white" name="name" placeholder="Name" value={form.name} onChange={handleChange} />
        <input className="p-2 rounded bg-slate-800 text-white" name="ssn" placeholder="SSN" value={form.ssn} onChange={handleChange} />
        <input className="p-2 rounded bg-slate-800 text-white" name="ein" placeholder="EIN (optional)" value={form.ein} onChange={handleChange} />
        <input className="p-2 rounded bg-slate-800 text-white" name="user_id" placeholder="User ID" value={form.user_id} onChange={handleChange} />
        <input className="p-2 rounded bg-slate-800 text-white" name="refund_amount" placeholder="Refund Amount" value={form.refund_amount} onChange={handleChange} type="number" />
        <button className="col-span-2 p-2 rounded bg-blue-600 hover:bg-blue-700 text-white font-bold" type="submit" disabled={loading}>{loading ? 'Checking...' : 'Run Pre-Submission Check'}</button>
      </form>
      {result && (
        <div className="mt-4 text-sm">
          <pre className="bg-slate-900 p-3 rounded overflow-x-auto text-white">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </section>
  );
}
