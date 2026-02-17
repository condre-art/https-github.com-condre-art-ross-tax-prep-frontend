# Tax Preparation Software Platform

This repository contains the initial scaffolding for a full-stack tax preparation platform with a FastAPI backend and a React (Vite + TypeScript) frontend.

## Structure

```
tax-software/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## Getting Started

See `tax-software/backend/README.md` and `tax-software/frontend/README.md` for setup instructions.

## Cloudflare Wrangler Secrets

If you deploy to Cloudflare (Workers/Pages), create the required secrets with Wrangler:

```bash
wrangler secret put JWT_SECRET
wrangler secret put PASSWORD_PEPPER
```

## Compliance & Data Privacy

This platform is designed with security and compliance in mind. Key policies:

- **Data Privacy:** User data is only collected for tax preparation and compliance purposes. No data is sold or shared with third parties except as required by law.
- **Data Retention:** Data is retained only as long as necessary for tax/legal requirements. Users may request deletion of their data by contacting support.
- **User Rights:** Users can request access to, export, or delete their data. Contact support for privacy requests.
- **Security:**
	- All secrets (JWT, password pepper, encryption keys) are managed via secure environment variables (Wrangler, Vercel, or AWS secrets).
	- S3 buckets and D1 DB access are restricted to least-privilege service accounts.
	- All sensitive actions are logged and auditable.
	- Dependencies are regularly scanned for vulnerabilities in CI/CD.
- **Compliance Contact:** For privacy or compliance questions, contact: [support@example.com](mailto:support@example.com)

See `docs/COMPLIANCE.md` for full details.
