#!/bin/bash

set -e

AWS_ACCOUNT_ID="$1"
AWS_REGION="$2"
REPO_NAME="$3"
TAG="${4:-latest}"

if [ -z "$AWS_ACCOUNT_ID" ] || [ -z "$AWS_REGION" ] || [ -z "$REPO_NAME" ]; then
    echo "Usage: deploy.sh <account_id> <region> <repo_name> [tag]"
    exit 1
fi

IMAGE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$TAG"
STACK_NAME="taggtraad"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
template="$script_dir/template.yml"

echo "Deploying stack '$STACK_NAME' to $AWS_REGION..."
echo "Image URI: $IMAGE_URI"

aws cloudformation deploy \
    --region "$AWS_REGION" \
    --stack-name "$STACK_NAME" \
    --template-file "$template" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        ImageUri="$IMAGE_URI" \
        TeamsWebhookUrl="$TEAMS_WEBHOOK_URL" \
        RequiredTags="$REQUIRED_TAGS"

echo "Done!"
