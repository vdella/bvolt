# BVOLT Security

This document defines the security baseline for BVOLT: how secrets are stored, how services authenticate, and how deployments are performed.

## Scope

This policy applies to:
- All BVOLT microservices and worker processes
- CI/CD pipelines (GitHub Actions)
- Any runtime environments (local dev, staging, production)
- Any credential used to access lab infrastructure, databases, or third-party systems

## Security principles

1. **No secrets in Git**
    - Never commit tokens, passwords, private keys, or `.env` files containing real values.
2. **Least privilege**
    - Each service has its own IAM role with only the permissions it requires.
3. **Short-lived credentials first**
    - Prefer role-based access (AWS IAM) and GitHub OIDC over static access keys.
4. **Separation by environment**
    - Dev, staging, and prod use distinct secrets and distinct roles.
5. **Auditability**
    - Secret access should be attributable to a role/session (CloudTrail + service logs).
6. **Rotation**
    - Any long-lived secret that cannot be eliminated must be rotated on a schedule.

---

## What is a secret vs configuration?

### Non-secret configuration (allowed in Git)
Examples:
- Service ports, log levels, timeouts
- Non-sensitive URLs and identifiers (e.g., InfluxDB URL, org/bucket name)
- Feature flags

### Secrets (never allowed in Git)
Examples:
- InfluxDB token
- Database credentials
- JWT signing keys / session secrets
- VPN / gateway credentials (lab polling)
- Webhook signing secrets
- Private keys

When in doubt: treat it as a secret.

---

## Secret storage policy

### Local development
Secrets are stored in a gitignored file:
- `.env.local` (recommended) or shell environment via `direnv`

A template is provided:
- `.env.example` (contains placeholders only)

Local files containing secrets must not be shared or uploaded to public locations.

### AWS runtime (staging/prod)
Secrets are stored in:
- **AWS Secrets Manager** (primary)
- **AWS SSM Parameter Store (SecureString)** (optional, for less sensitive or cheaper parameters)

Production secrets must not be stored in:
- GitHub Secrets (except CI bootstrap)
- EC2 instance filesystem
- Docker images or build layers
- Kubernetes ConfigMaps

---

## Naming conventions

### Secrets Manager (recommended)
Use hierarchical names (slashes are a naming convention):
- `bvolt/{env}/{service}/{secret_name}`

Examples:
- `bvolt/prod/api/jwt_signing_key`
- `bvolt/prod/ingestion/influx_token`
- `bvolt/prod/shared/influx_readonly`

### Parameter Store (optional)
- `/bvolt/{env}/{service}/{param_name}`

Examples:
- `/bvolt/prod/api/influx_url`
- `/bvolt/prod/api/influx_bucket`

---

## Runtime access model (the “pointer” pattern)

Services do not store secret values in source code or config files.

Instead, the service receives:
- the **name** of the secret (non-secret) via environment variable, e.g.:

```bash
INFLUX_TOKEN_SECRET_ID=bvolt/prod/ingestion/influx_token
JWT_SIGNING_KEY_SECRET_ID=bvolt/prod/api/jwt_signing_key
```