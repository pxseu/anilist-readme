#!/bin/bash

echo "[TEST_SCRIPT]: Starting the project"
echo ""

DEV=true INPUT_USER_ID=889921 INPUT_GH_TOKEN=test INPUT_COMMIT_EMAIL=test INPUT_COMMIT_USERNAME=test INPUT_PREFERRED_LANGUAGE=english INPUT_MAX_POST_COUNT=5 INPUT_COMMIT_MESSAGE=update python3 .

echo ""
echo "[TEST_SCRIPT]: Done"