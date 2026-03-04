import sys
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# --- Configuration ---
MINIO_URL = "http://local-s3-service.ezdata-system.svc.cluster.local:30000" 
TOKEN_FILE = "/etc/secrets/ezua/.auth_token"
SECRET_KEY = "s3"

def get_access_key():
    try:
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: Access key file not found at {TOKEN_FILE}")
        sys.exit(1)

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=MINIO_URL,
        aws_access_key_id=get_access_key(),
        aws_secret_access_key=SECRET_KEY
    )

def list_buckets():
    s3 = get_s3_client()
    try:
        response = s3.list_buckets()
        # SWAP: Timestamp first, then Name
        print(f"{'Creation Date':<30} | {'Bucket Name'}")
        print("-" * 60)
        for bucket in response['Buckets']:
            # Render CreationDate (stringified) followed by the Name
            print(f"{str(bucket['CreationDate']):<30} | {bucket['Name']}")
    except Exception as e:
        print(f"Error listing buckets: {e}")

def list_files(bucket_name):
    s3 = get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            print(f"Bucket '{bucket_name}' is empty or does not exist.")
            return

        # SWAP: Size first, then File Name
        print(f"{'Size (Bytes)':>12} | {'File Name'}")
        print("-" * 60)
        for obj in response['Contents']:
            # Render Size followed by the Key (Filename)
            print(f"{obj['Size']:>12} | {obj['Key']}")
    except ClientError as e:
        print(f"Error accessing bucket '{bucket_name}': {e}")

def main():
    # Use sys.argv[0] to dynamically get the script name
    script_name = sys.argv[0]

    if len(sys.argv) < 2:
        print(f"Usage:")
        print(f"  python {script_name} buckets")
        print(f"  python {script_name} files <bucket-name>")
        return

    command = sys.argv[1].lower()

    if command == "buckets":
        list_buckets()
    elif command == "files":
        if len(sys.argv) < 3:
            print(f"Error: Please provide a bucket name.")
            print(f"Usage: python {script_name} files <bucket-name>")
        else:
            list_files(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print(f"Try: python {script_name} buckets")

if __name__ == "__main__":
    main()