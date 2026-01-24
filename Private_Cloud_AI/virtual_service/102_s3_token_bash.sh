#!/bin/bash

# 1. Check if PCAI_SECRET_TOKEN environment variable exists
if [[ -z "$PCAI_SECRET_TOKEN" ]]; then
    echo "Error: Environment variable 'PCAI_SECRET_TOKEN' is not set."
    echo "Please run: export PCAI_SECRET_TOKEN='your_token_here'"
    exit 1
fi

# 2. Check for exactly two command-line arguments
if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 <path_to_refresh_token_file> <keycloak_domain>"
    echo "Example: $0 ./tokens.txt sso.appliance.local"
    exit 1
fi

# Assign arguments to descriptive variables
export TOKEN_FILE="$1"
export KC_ADDR="$2"
export SECRET="$PCAI_SECRET_TOKEN"

# --- DEBUG START (Remove these lines once fixed) ---
 echo "DEBUG: Filename detected: $TOKEN_FILE"
 echo "DEBUG: Domain detected: $KC_ADDR"
 echo "DEBUG: SECRET detected: $SECRET"

# --- DEBUG END ---


# 3. Read the file and load it into an environment variable
if [[ -f "$TOKEN_FILE" ]]; then
    export PCAI_REFRESH_TOKEN=$(cat "$TOKEN_FILE")
    echo "Success: refresh_token loaded from $TOKEN_FILE"
    echo $PCAI_REFRESH_TOKEN
else
    echo "Error: File '$TOKEN_FILE' not found."
    exit 1
fi

# ---------------------------------------------------------
# 4. get PCAI_ACCESS_TOKEN and set in AWS variables for S3 access
# ---------------------------------------------------------

response_json=$(curl -k --data \
"grant_type=refresh_token&client_id=ua&refresh_token=$PCAI_REFRESH_TOKEN&client_secret=$PCAI_SECRET_TOKEN" \
https://$KC_ADDR/realms/UA/protocol/openid-connect/token)

export PCAI_ACCESS_TOKEN=$(echo "$response_json" | jq -r '.access_token')
echo "PCAI_ACCESS_TOKEN received: token is $PCAI_ACCESS_TOKEN"

export AWS_ACCESS_KEY_ID=$PCAI_ACCESS_TOKEN
export AWS_SECRET_ACCESS_KEY=“s3”


echo "DEBUG: AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID"
echo "DEBUG: AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY"
echo "AWS secret and access key environment variables set. You may use AWS CLI now."


# ---------------------------------------------------------

# 5. Print final message
echo "Process completed for domain: $KC_ADDR"