#!/bin/bash

set -e

echo "--- Publishing images to Stockholm ---"

AWS_REGION="eu-north-1"
AWS_ACCOUNT_ID="952457084211"
REPO_NAME="taggtraad/validator"
TAG="latest"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cmd="$script_dir/publish.sh" 
cmd+=" $AWS_ACCOUNT_ID"
cmd+=" $AWS_REGION"
cmd+=" $REPO_NAME"

$cmd