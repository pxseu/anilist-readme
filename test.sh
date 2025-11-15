#!/bin/bash

set -e

echo "[TEST_SCRIPT]: Starting the project"
echo ""

python -m unittest

DEV=true INPUT_USER_ID=889921 INPUT_GH_TOKEN=test INPUT_PREFERRED_LANGUAGE=english INPUT_TIMEZONE=UTC python3 .

echo ""
echo "[TEST_SCRIPT]: Done"