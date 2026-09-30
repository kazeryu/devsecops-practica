#!/usr/bin/env bash
set -euo pipefail
RG="${RG:-rg-devsecops-m4}"
LOC="${LOC:-westeurope}"
KV="${KV:-kv-devsecops}"
az group create -n "$RG" -l "$LOC"
az keyvault create -n "$KV" -g "$RG" -l "$LOC" --enable-rbac-authorization false
az keyvault secret set --vault-name "$KV" --name db-connection-string \
  --value "Server=db;Database=app;User=appuser;Password=ChangeMe!"
echo "AZURE_KEYVAULT_URL=https://${KV}.vault.azure.net/"
