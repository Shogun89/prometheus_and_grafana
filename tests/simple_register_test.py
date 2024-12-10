import requests
import json
import random
import string

def test_register(email: str, password: str, BASE_URL: str):

    print("Testing user registration...")
    
    try:
        # Send registration request
        response = requests.post(
            f"{BASE_URL}/auth/register",
            headers={"Content-Type": "application/json"},
            json={"email": email, "password": password}
        )
        
        # Print results
        print(f"\nStatus Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the auth service")
    except Exception as e:
        print(f"Error: {str(e)}")

def get_token(email: str, password: str, BASE_URL: str) -> str:
    print(f"\nGetting token for user: {email}")
    
    login_data = {
        "username": email,
        "password": password,
        "grant_type": "",
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
    
    try:
        # Send login request
        response = requests.post(
            f"{BASE_URL}/auth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=login_data
        )
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("Token obtained successfully")
            return token
        else:
            print(f"Failed to get token. Status Code: {response.status_code}")
            print("Response:", json.dumps(response.json(), indent=2))
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the auth service")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def generate_test_credentials() -> dict:
    """
    Generate unique test credentials with a valid password that meets all requirements.
    
    Returns:
        tuple: Tuple containing email and password
    """
    # Generate random string for email
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"test_{random_string}@example.com"
    
    # Generate password meeting all requirements
    lowercase = ''.join(random.choices(string.ascii_lowercase, k=4))
    uppercase = ''.join(random.choices(string.ascii_uppercase, k=4))
    digits = ''.join(random.choices(string.digits, k=4))
    special = ''.join(random.choices("!@#$%^&*()_+-=", k=2))
    
    # Combine all parts and s   huffle
    password = list(lowercase + uppercase + digits + special)
    random.shuffle(password)
    password = ''.join(password)
    
    return email, password

def test_backend(email: str, token: str, BASE_URL: str):
    print(f"\nTesting backend with token for user: {email}")
    url = f"{BASE_URL}/api/users"
    print(f"Making request to: {url}")

    try:
        # Create user in backend
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        print(f"Headers: {headers}")
        
        response = requests.post(
            url,
            headers=headers,
            json={
                "email": email,
                "is_active": True,
                "password": "dummy_password"
            }
        )
        print(f"User creation status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        try:
            print("Response:", json.dumps(response.json(), indent=2))
        except:
            print("Raw response:", response.text)
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the backend service")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Starting test...")
    BASE_AUTH_URL = "http://localhost:80/authentication"
    BASE_BACKEND_URL = "http://localhost:80/backend"

    # Generate unique test credentials
    test_email, test_password = generate_test_credentials()
    print("Test credentials generated")
    print("Email: ", test_email)
    print("Password: ", test_password)
    test_register(test_email, test_password, BASE_AUTH_URL)
    # Example of getting a token
    token = get_token(test_email, test_password, BASE_AUTH_URL)
    if token:
        print(f"\nToken: {token}")
        test_backend(test_email, token, BASE_BACKEND_URL)
        print("Backend test completed")
    else:
        print("Failed to get token")


