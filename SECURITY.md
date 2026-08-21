# Security policy

## Reporting

Report credentials, exposed private data, unsafe file handling or dependency vulnerabilities privately to the team lead. Do not open a public issue containing secrets.

## Repository rules

- Never commit `.env`, tokens, passwords or database dumps.
- Use `.env.example` for variable names and safe placeholders.
- Validate uploaded AOI and geospatial files before processing.
- Apply explicit size limits to uploads and analysis regions.
- Treat remote URLs as untrusted input.
- Record licenses and terms for external data.
- Do not publish precise private-property or field-survey data without authorization.

This hackathon scaffold is not production-hardened and must not be deployed as a public service without authentication, rate limiting, storage isolation and security review.
