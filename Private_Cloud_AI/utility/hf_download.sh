#!/bin/bash
# Use to download huggingface model snapshot

# Check for the required 3 arguments
if [ "$#" -ne 3 ]; then
    echo "Usage:   $0 <model_name> <hf_token> <target_path>"
    echo "Example: $0 google/gemma-3-4b-it hf_xxxxxx /mnt/shared/models"
    exit 1
fi

# Assigning parameters to readable variables
MODEL_NAME=$1
HF_TOKEN=$2
TARGET_PATH=$3

echo "--- Initializing Environment ---"

# 1. Ensure the target directory exists
if [ ! -d "$TARGET_PATH" ]; then
    echo "Target directory does not exist. Creating: $TARGET_PATH"
    mkdir -p "$TARGET_PATH"
fi

# 2. Upgrade the Hugging Face CLI
pip install --upgrade huggingface_hub

# 3. Export Environment Variables (as seen in your notebook)
export HF_HOME="$TARGET_PATH"
export HF_HUB_DISABLE_XET=1
export HF_TOKEN="$HF_TOKEN"
export HF_DEBUG=1

echo "--- Starting Download ---"
echo "Model: $MODEL_NAME"
echo "Path:  $TARGET_PATH"

# 4. Execute the download
# Using --local-dir to force the files into your specific path
hf download "$MODEL_NAME"

# Check if the command succeeded
if [ $? -eq 0 ]; then
    echo "------------------------------------------------"
    echo "SUCCESS: $MODEL_NAME is ready at $TARGET_PATH"
else
    echo "------------------------------------------------"
    echo "ERROR: Download failed. Check your token or model name."
    exit 1
fi