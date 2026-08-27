# Security

This project is production-oriented reference software, not a compliance certification. It demonstrates signed authentication, tenant-scoped retrieval, role-bearing security context, bounded uploads, citation verification, and a place for audit logging.

Retrieved documents are untrusted data and must never override system policy. Hosted deployments should add managed identity, Key Vault, PostgreSQL RLS, malware scanning, rate limiting, network policies, secret scanning, and formal threat-model review. Technical controls do not by themselves establish GDPR or other legal compliance.
