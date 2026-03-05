import requests
import json
import urllib3

# This line specifically disables the warning you see in the terminal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MODEL_ENDPOINT = "https://test-delete-3.sales-enablemen-e5aec00c.serving.prod.lg-pcai.hou"
API_PATH = "/v1/chat/completions"
TOKEN_FILE = "../tokens/token1.txt"

with open(TOKEN_FILE, "r") as f:
    AUTH_TOKEN = f.read().strip()

BODY_DATA = {
    "model": "meta/llama-3.1-8b-instruct",
    "messages": [
        {"role": "system", "content": "You are a software engineer"},
        {"role": "user", "content": "How far is the moon from earth"}
    ],
    "max_tokens": 1024
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}",
}

# Making the request with verify=False to bypass SSL certificate checks
response = requests.post(
    f"{MODEL_ENDPOINT}{API_PATH}", 
    headers=headers, 
    data=json.dumps(BODY_DATA), 
    verify=False
)

print("\n ------- \n ")

# Pretty printing the JSON response with an indent of 4
print(json.dumps(json.loads(response.text), indent=4))