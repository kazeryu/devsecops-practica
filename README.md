# devsecops-practica (M4 P4)

- Gitleaks (`.gitleaks.toml` + workflow que falla si hay secretos)
- Dockerfile Alpine no-root
- Trivy en CI (falla con CRITICAL/HIGH)
- App Flask lee secreto desde **AWS Secrets Manager** (`AWS_SECRET_NAME`)

> El enunciado pedía Azure Key Vault; se usa AWS porque la suscripción Azure
> responde `SubscriptionNotFound` (no usable). Secrets Manager es el equivalente.
