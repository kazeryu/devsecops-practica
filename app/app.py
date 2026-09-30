"""API Flask que lee un secreto desde Azure Key Vault (DefaultAzureCredential)."""
import os
from flask import Flask, jsonify

app = Flask(__name__)

VAULT_URL = os.getenv("AZURE_KEYVAULT_URL", "")
SECRET_NAME = os.getenv("AZURE_SECRET_NAME", "db-connection-string")


def get_secret() -> str:
    """Obtiene el secreto desde Key Vault. Credenciales vía DefaultAzureCredential / env."""
    if not VAULT_URL:
        # Fallback local solo para demos sin vault (no usar en prod)
        return os.getenv("DB_CONNECTION_STRING", "")
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    client = SecretClient(vault_url=VAULT_URL, credential=DefaultAzureCredential())
    return client.get_secret(SECRET_NAME).value


@app.get("/")
def index():
    return jsonify(status="ok", app="devsecops-practica")


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/config")
def config():
    secret = get_secret()
    # Nunca devolver el secreto completo en claro en producción; aquí se enmascara para evidencia
    masked = (secret[:4] + "****" + secret[-4:]) if secret and len(secret) > 8 else ("****" if secret else "missing")
    return jsonify(
        vault=VAULT_URL or "env-fallback",
        secret_name=SECRET_NAME,
        secret_masked=masked,
        source="keyvault" if VAULT_URL else "env",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
