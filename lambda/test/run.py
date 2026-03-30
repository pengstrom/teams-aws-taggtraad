#!/usr/bin/env python3
"""
Local test runner for the Lambda handler.

Usage:
    python -m test.run <event-name>

Example:
    python -m test.run create-image

Events are loaded from test/<event-name>.json.
Environment variables are loaded from .env in the lambda root directory.
"""

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from aws_lambda_powertools.utilities.typing import LambdaContext

TEST_DIR = Path(__file__).parent


@dataclass
class FakeLambdaContext(LambdaContext):
    function_name: str = "local-test"
    function_version: str = "$LATEST"
    invoked_function_arn: str = "arn:aws:lambda:eu-north-1:000000000000:function:local-test"
    memory_limit_in_mb: int = 128
    aws_request_id: str = "local-test-request-id"
    log_group_name: str = "/aws/lambda/local-test"
    log_stream_name: str = "local"
    _remaining_time: int = field(default=300000, repr=False)

    def get_remaining_time_in_millis(self):
        return self._remaining_time


def load_env():
    env_file = TEST_DIR.parent / ".env"
    if not env_file.exists():
        print(f"Error: {env_file} not found. Create a .env file in the lambda directory.")
        sys.exit(1)
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            value = value.strip()
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            os.environ[key.strip()] = value


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m test.run <event-name>")
        print(f"\nAvailable events:")
        for f in sorted(TEST_DIR.glob("*.json")):
            print(f"  {f.stem}")
        sys.exit(1)

    event_name = sys.argv[1]
    event_file = TEST_DIR / f"{event_name}.json"
    if not event_file.exists():
        print(f"Error: Event file not found: {event_file}")
        sys.exit(1)

    load_env()

    with open(event_file) as f:
        event = json.load(f)

    from index import handler

    print(f"--- Running event: {event_name} ---")
    result = handler(event, FakeLambdaContext())
    print(f"--- Result ---")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
