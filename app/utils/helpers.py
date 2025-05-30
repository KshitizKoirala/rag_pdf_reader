import base64
import hashlib
import hmac
import json
import os

from app.config import SECRET_KEY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(BASE_DIR, '../auth/api-keys.json')


def create_api_key(email: str, password: str):
    encoded_key = create_hashed_password(password)
    # Load the api-key JSON file
    with open(json_file_path) as f:
        data = json.load(f)

    data.append({"email": email, "key": encoded_key})

    # update the file
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=2)

    return encoded_key


def get_if_api_key_exists(email: str):
    # Load the api-key JSON file
    with open(json_file_path) as f:
        data = json.load(f)

    for record in data:
        if record["email"] == email:
            return record["key"]

    return False


def get_email_from_api_key(api_key: str):
    # Load the api-key JSON file
    with open(json_file_path) as f:
        data = json.load(f)

    for record in data:
        if record["key"] == api_key:
            return record["email"]

    return False


def create_hashed_password(password):
    # Encode password using HMAC + SHA256
    encoded_bytes = hmac.new(
        SECRET_KEY, password.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(encoded_bytes).decode()


def verify_api_key(api_key, password):
    encoded_key = create_hashed_password(password)

    if api_key != encoded_key:
        return False

    return True
