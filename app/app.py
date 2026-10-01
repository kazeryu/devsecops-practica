"""API Flask que lee un secreto desde AWS Secrets Manager (credenciales IAM / env)."""
import os
from flask import Flask, jsonify

app = Flask(__name__)

SECRET_NAME = os.getenv("AWS_SECRET_NAME", "devsecops/db-connection-string")
AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "eu-west-1"))
USE_SECRETS_MANAGER = os.getenv("USE_AWS_SECRETS_MANAGER", "1") == "1"


def get_secret() -> tuple[str, str]:
    """Devuelve (valor, source). Credenciales vía IAM role / ~/.aws / env (sin secretos en código)."""
    if not USE_SECRETS_MANAGER:
        return os.getenv("DB_CONNECTION_STRING", ""), "env"

    import boto3
    from botocore.exceptions import ClientError

    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    try:
        resp = client.get_secret_value(SecretId=SECRET_NAME)
        return resp.get("SecretString") or "", "secretsmanager"
    except ClientError as exc:
        # Fallback solo para demos locales si el secreto no es accesible
        fallback = os.getenv("DB_CONNECTION_STRING", "")
        if fallback:
            return fallback, "env-fallback"
        raise RuntimeError(f"No se pudo leer el secreto: {exc}") from exc


def mask(secret: str) -> str:
    if not secret:
        return "missing"
    if len(secret) > 8:
        return secret[:4] + "****" + secret[-4:]
    return "****"


@app.get("/")
def index():
    return jsonify(status="ok", app="devsecops-practica")


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/config")
def config():
    secret, source = get_secret()
    return jsonify(
        provider="aws-secrets-manager",
        region=AWS_REGION,
        secret_name=SECRET_NAME,
        secret_masked=mask(secret),
        source=source,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
