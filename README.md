# Aori Python SDK

The Aori Python SDK provides a convenient interface for interacting with the Aori API, allowing developers to easily integrate Aori's functionalities into their Python applications.

## Features

- Authentication with API keys
- Operations for orders: create, take, cancel
- Viewing and subscribing to orderbook updates
- Requesting quotes for potential orders

## Installation

To install the Aori Python SDK, run the following command:

```bash
pip install aori-sdk-py
```

## Configuration

Before using the SDK, you need to configure it with your Aori API key and private key. There are two ways to do this:

### Using Environment Variables

1. Create a `.env` file in your project root.
2. Add your Aori API key and private key to the `.env` file as shown below:

```plaintext
AORI_API_KEY=your_aori_api_key_here
PRIVATE_KEY=your_private_key_here
```

3. Load the environment variables in your application:

```python
from dotenv import load_dotenv
load_dotenv()
```

4. Initialize the SDK:

```python
from aori_sdk_py.sdk import AoriSDK

sdk = AoriSDK()
```

### Passing Directly


Alternatively, you can pass your API key and private key directly when creating an instance of the SDK:

```python
from aori_sdk_py.sdk import AoriSDK

sdk = AoriSDK(api_key='your_aori_api_key_here', private_key='your_private_key_here')
```

## Usage

Here are some examples of how to use the Aori Python SDK:

### Test Connectivity

To test the connectivity to the Aori API, you can use the following code snippet:

```python
from aori_sdk_py.sdk import AoriSDK

sdk = AoriSDK(api_key='your_aori_api_key_here')
connectivity_response = sdk.test_connectivity()
print(connectivity_response)
```

This should return a response indicating successful connectivity, such as `{'id': 1, 'result': 'aori_pong'}`.

### Create a New Order

```python
from aori_sdk_py.sdk import AoriOrder, AoriSDK

sdk = AoriSDK(api_key='your_aori_api_key_here')
new_order = AoriOrder(
    offerer="0x...",
    inputToken="0x...",
    inputAmount="1000000000000000000",  # 1 Token in Wei
    inputChainId=1,
    inputZone="0x...",
    outputToken="0x...",
    outputAmount="500000000000000000",  # 0.5 Token in Wei
    outputChainId=1,
    outputZone="0x...",
    startTime="1622548800",
    endTime="1625130800",
    salt="123456789",
    counter=0,
    toWithdraw=False,
    signature="0x...",
    isPublic=True
)

order_response = sdk.make_order(new_order)
print(order_response)
```

### Subscribe to Orderbook Updates

```python
sdk.subscribe_orderbook()
```

## Testing

To run a basic connectivity test, ensure you have your API key set in the `.env` file or passed directly to the `AoriSDK` instance. Here's an example test script:

```python
import os
from dotenv import load_dotenv
from aori_sdk_py.sdk import AoriSDK

# Load environment variables
load_dotenv()

def test_aori_ping():
    api_key = os.getenv('AORI_API_KEY', 'your_default_api_key_here')
    sdk = AoriSDK(api_key=api_key)
    response = sdk.test_connectivity()
    print(response)
    assert 'result' in response, "Ping failed, no result found in response"
    assert response['result'] == 'aori_pong', "Ping failed, did not receive expected 'aori_pong' response"

if __name__ == "__main__":
    test_aori_ping()
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
