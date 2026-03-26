#!/bin/bash

set -e

AWS_ACCOUNT_ID="$1"
AWS_REGION="$2"
REPO_NAME="$3"
TAG="${4:-latest}"
export AWS_PAGER=""

if [ -z "$AWS_ACCOUNT_ID" ] || [ -z "$AWS_REGION" ] || [ -z "$REPO_NAME" ]; then
    echo "Usage: publish.sh <account_id> <region> <repo_name> [tag]"
    exit 1
fi

ECR_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
IMAGE="$ECR_URL/$REPO_NAME:$TAG"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
lambda_dir="$script_dir/.."

echo "Logging in to ECR..."
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_URL"

echo "Ensuring ECR repository exists..."
aws ecr describe-repositories --region "$AWS_REGION" --repository-names "$REPO_NAME" 2>/dev/null || \
    aws ecr create-repository --region "$AWS_REGION" --repository-name "$REPO_NAME"

echo "Building and pushing image: $IMAGE"
docker buildx build --platform linux/arm64 --provenance=false -t "$IMAGE" --push "$lambda_dir"

echo "Done!"
