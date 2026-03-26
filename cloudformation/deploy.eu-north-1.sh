#!/bin/bash

set -e

echo "--- Deploying stack to Stockholm ---"

AWS_REGION="eu-north-1"
AWS_ACCOUNT_ID="952457084211"
REPO_NAME="taggtraad/validator"
TAG="latest"
TEAMS_WEBHOOK_URL="https://default9c19ad122e734b3fa65e71f0aef98d.2b.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/d60a1a0146844f94be460bd57c03eb08/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=G2ic4IsU2Vl4mYOLe8cX2AR096slGwvfbufgvOfr0lA"
REQUIRED_TAGS='["Project", "Customer", "Environment"]'

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cmd="$script_dir/deploy.sh" 
cmd+=" $AWS_ACCOUNT_ID"
cmd+=" $AWS_REGION"
cmd+=" $REPO_NAME"

$cmd