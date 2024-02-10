import os
from dotenv import load_dotenv
from aori_sdk_py.sdk import AoriSDK

# Load environment variables
load_dotenv()

def test_aori_ping():
    # Access environment variables using os.getenv
    api_key = os.getenv('AORI_API_KEY', 'your_default_api_key_here')
    sdk = AoriSDK(api_key=api_key)  # Use the API key from environment variables
    response = sdk.test_connectivity()
    print(response)
    assert 'result' in response, "Ping failed, no result found in response"
    assert response['result'] == 'aori_pong', "Ping failed, did not receive expected 'aori_pong' response"
    
if __name__ == "__main__":
    test_aori_ping()