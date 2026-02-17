#!/usr/bin/env bash
set -euo pipefail

STACK_NAME="${1:-erp-cicd-stack}"
TEMPLATE_FILE="${2:-cloudformation/erp-cicd.yaml}"
REGION="${AWS_REGION:-ap-south-1}"

start_create=$(date +%s)
aws cloudformation create-stack \
  --stack-name "$STACK_NAME" \
  --template-body "file://$TEMPLATE_FILE" \
  --capabilities CAPABILITY_NAMED_IAM \
  --region "$REGION"

aws cloudformation wait stack-create-complete --stack-name "$STACK_NAME" --region "$REGION"
end_create=$(date +%s)

start_delete=$(date +%s)
aws cloudformation delete-stack --stack-name "$STACK_NAME" --region "$REGION"
aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME" --region "$REGION"
end_delete=$(date +%s)

create_time=$((end_create - start_create))
delete_time=$((end_delete - start_delete))

echo "Stack create time (sec): $create_time"
echo "Stack delete time (sec): $delete_time"
