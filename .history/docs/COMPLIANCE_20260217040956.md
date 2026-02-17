# Compliance, Security, and Data Privacy Policy

## Endpoint Protection & Auditing
- All sensitive API endpoints require authentication (JWT Bearer token).
- Role-based access control (RBAC) is fully enforced for all sensitive endpoints. Each API route specifies required roles, and access is denied if the user's role does not match. See backend/app/main.py and router files for details.
- All sensitive actions (employee/payroll changes, uploads, certificate generation, etc.) are logged using Python's logging module with an "AUDIT" tag.
- Audit logs are stored in application logs and can be exported for compliance review.

## CI/CD Automation & Security
- CI/CD pipeline (GitHub Actions) runs on every push/PR:
	- Dependency vulnerability scanning (`pip-audit`, `npm audit`)
	- Linting and test coverage enforcement
	- Secret scanning (gitleaks)
	- Deployment is blocked if compliance/security checks fail

## Policy Review
- This policy is reviewed and updated regularly to ensure compliance with legal, regulatory, and industry standards.

## Data Privacy
- User data is collected only for tax preparation and compliance purposes.
- No data is sold or shared with third parties except as required by law.
- Users may request access to, export, or deletion of their data by contacting support.

## Data Retention
- Data is retained only as long as required by tax/legal regulations.
- Data is deleted upon user request, subject to legal requirements.

## Security Practices
- All secrets (JWT, password pepper, encryption keys) are managed via secure environment variables (Wrangler, Vercel, AWS, or local .env for development).
- S3 buckets and D1 DB access are restricted to least-privilege service accounts.
- Sensitive actions (admin changes, data exports, etc.) are logged and auditable.
- Dependencies are regularly scanned for vulnerabilities in CI/CD.
- No plaintext secrets or credentials are stored in the codebase.

## User Rights
- Users may request access to, export, or deletion of their data.
- Contact [support@example.com](mailto:support@example.com) for privacy or compliance requests.

## Compliance Contact
- For privacy or compliance questions, contact: [support@example.com](mailto:support@example.com)


## RBAC Enforcement Details
- All sensitive endpoints (employee, payroll, paystub, timecard, IRS certificate, XML upload, pre-submission check, etc.) require authentication and explicit role authorization.
- Roles include: admin, staff, ERO, client, and anon (see backend/app/blueprint.py).
- RBAC is enforced using a dependency (`require_role`) that checks the user's role from the JWT token.
- Unauthorized access attempts are logged and denied with HTTP 403.

## Review & Updates
This policy is reviewed regularly and updated as needed to meet legal and regulatory requirements.
