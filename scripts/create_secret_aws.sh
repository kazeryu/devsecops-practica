#!/usr/bin/env bash
# Crear secreto en AWS Secrets Manager (cuenta personal / Tokio School)
# Equivalente a Azure Key Vault kv-devsecops
set -euo pipefail
PROFILE="${AWS_PROFILE:-devops-personal}"
REGION="${AWS_REGION:-eu-west-1}"
NAME="${AWS_SECRET_NAME:-devsecops/db-connection-string}"
VALUE="${SECRET_VALUE:-Server=db;Database=app;User=appuser;Password=ChangeMe!}"

export AWS_PROFILE="$PROFILE"

echo "Cuenta:"
aws sts get-caller-identity --output table

if aws secretsmanager describe-secret --secret-id "$NAME" --region "$REGION" >/dev/null 2>&1; then
  aws secretsmanager put-secret-value \
    --secret-id "$NAME" \
    --secret-string "$VALUE" \
    --region "$REGION"
  echo "Actualizado: $NAME"
else
  aws secretsmanager create-secret \
    --name "$NAME" \
    --description "M4 P4 DevSecOps — secreto de conexion DB (Tokio School)" \
    --secret-string "$VALUE" \
    --region "$REGION"
  echo "Creado: $NAME"
fi

echo "AWS_PROFILE=$PROFILE"
echo "AWS_SECRET_NAME=$NAME"
echo "AWS_REGION=$REGION"
aws secretsmanager describe-secret --secret-id "$NAME" --region "$REGION" \
  --query '{Name:Name,ARN:ARN}' --output table
