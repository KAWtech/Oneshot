import requests
import json
import random
import string
import os

# Function to generate a random string
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

# Generate random username and password
random_username = generate_random_string(6)
random_password = generate_random_string(12)

# CVAT HOST
CVAT_HOST = os.getenv('CVAT_HOST')

# Define the URL and payload
url = f"http://{CVAT_HOST}:8080/api/auth/register?org="
payload = {
    "username": random_username,
    "first_name": "OneShot",
    "last_name": "User",
    "email": f"{random_username}@kawtech.io",
    "password1": random_password,
    "password2": random_password,
    "confirmations": []
}

# Define the headers
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Origin': f"http://{CVAT_HOST}:8080",
    'Content-Type': 'application/json',
    'Authorization': '',  # Assuming no value for Authorization based on the given CURL command
    'Referer': 'http://192.168.1.165:8080/auth/register',
    'Content-Length': '170',
    'Host': '192.168.1.165:8080',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Save the credentials to a JSON file
credentials = {
    "username": payload["username"],
    "email": payload["email"],
    "password": payload["password1"]
}
with open("flask/cvat_credentials.json", "w") as f:
    json.dump(credentials, f)

# Print the response
print("Status code:", response.status_code)
print("Response text:", response.text)

with open("flask/cvat_credentials.json", 'r') as f:
    credentials = json.load(f)
    username = credentials.get("username", "")
    password = credentials.get("password", "")
    print("----------------------------------------------------------------------------------------------")
    print("CVAT user has been created!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("----------------------------------------------------------------------------------------------")
