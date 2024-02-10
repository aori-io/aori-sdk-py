import requests
import json
from dotenv import load_dotenv
import os
import websocket

# Load environment variables
load_dotenv()

class AoriOrder:
    """Class for Aori orders."""
    def __init__(self, offerer, inputToken, inputAmount, inputChainId, inputZone, outputToken, outputAmount, outputChainId, outputZone, startTime, endTime, salt, counter=None, toWithdraw=None, signature=None, isPublic=None):
        self.offerer = offerer
        self.inputToken = inputToken
        self.inputAmount = inputAmount
        self.inputChainId = inputChainId
        self.inputZone = inputZone
        self.outputToken = outputToken
        self.outputAmount = outputAmount
        self.outputChainId = outputChainId
        self.outputZone = outputZone
        self.startTime = startTime
        self.endTime = endTime
        self.salt = salt
        self.counter = counter
        self.toWithdraw = toWithdraw
        self.signature = signature
        self.isPublic = isPublic

class AoriSDK:
    def __init__(self, api_key=None, private_key=None):
        self.api_url = "https://api.aori.io"
        self.api_key = api_key if api_key else os.getenv("AORI_API_KEY")
        self.private_key = private_key if private_key else os.getenv("PRIVATE_KEY")
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}' if self.api_key else None
        }

    def authenticate(self, api_key):
        """Set the API key for authentication."""
        self.api_key = api_key
        self.headers['Authorization'] = f'Bearer {self.api_key}'

    def test_connectivity(self):
        """Test connectivity to the API."""
        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "aori_ping",
            "params": []
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def get_account_orders(self):
        """Retrieve orders associated with the account."""
        payload = {
            "id": 1,  # This can be made dynamic for actual use
            "jsonrpc": "2.0",
            "method": "aori_accountOrders",
            "params": [{
                "apiKey": self.api_key,
            }]
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def view_orderbook(self, chain_id=None, base=None, quote=None, side=None, limit=100):
        """Retrieve the current orderbook."""
        params = {
            "chainId": chain_id,
            "query": {
                "base": base,
                "quote": quote
            },
            "side": side,
            "limit": limit
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        if 'query' in params:
            params['query'] = {k: v for k, v in params['query'].items() if v is not None}

        payload = {
            "id": 1,  # This can be made dynamic for actual use
            "jsonrpc": "2.0",
            "method": "aori_viewOrderbook",
            "params": [params]
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def make_order(self, order):
        """Create a new order."""
        payload = {
            "id": 1,  # This can be made dynamic for actual use
            "jsonrpc": "2.0",
            "method": "aori_makeOrder",
            "params": [{
                "apiKey": self.api_key,
                "order": {
                    "offerer": order.offerer,
                    "inputToken": order.inputToken,
                    "inputAmount": order.inputAmount,
                    "inputChainId": order.inputChainId,
                    "inputZone": order.inputZone,
                    "outputToken": order.outputToken,
                    "outputAmount": order.outputAmount,
                    "outputChainId": order.outputChainId,
                    "outputZone": order.outputZone,
                    "startTime": order.startTime,
                    "endTime": order.endTime,
                    "salt": order.salt,
                    "counter": order.counter,
                    "toWithdraw": order.toWithdraw,
                    "signature": order.signature,
                    "isPublic": order.isPublic
                }
            }]
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def take_order(self, order_id, taker, amount, signature):
        """Take an existing order."""
        payload = {
            "id": 1,  # This can be made dynamic for actual use
            "jsonrpc": "2.0",
            "method": "aori_takeOrder",
            "params": [{
                "apiKey": self.api_key,
                "order_id": order_id,
                "taker": taker,
                "amount": amount,
                "signature": signature
            }]
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def cancel_order(self, order_id):
        """Cancel an existing order."""
        payload = {
            "id": 1,  # This can be made dynamic for actual use
            "jsonrpc": "2.0",
            "method": "aori_cancelOrder",
            "params": [{
                "apiKey": self.api_key,
                "orderId": order_id,
            }]
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def request_quote(self, inputToken, outputToken, inputAmount, chainId):
        """Request a quote for a potential order."""
        payload = {
            "id": 1,  # This can be made dynamic for actual use
            "jsonrpc": "2.0",
            "method": "aori_requestQuote",
            "params": [{
                "apiKey": self.api_key,
                "inputToken": inputToken,
                "outputToken": outputToken,
                "inputAmount": inputAmount,
                "chainId": chainId
            }]
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def subscribe_orderbook(self):
        """Subscribe to the orderbook updates."""
        ws_url = "wss://api.aori.io/ws"  # Hypothetical WebSocket URL for Aori API
        def on_message(ws, message):
            print("Received message:", message)
        
        def on_error(ws, error):
            print("Error:", error)
        
        def on_close(ws):
            print("### closed ###")
        
        def on_open(ws):
            print("Opened connection")
            subscribe_message = json.dumps({
                "id": 1,
                "jsonrpc": "2.0",
                "method": "aori_subscribeOrderbook",
                "params": []  # Add necessary parameters here
            })
            ws.send(subscribe_message)
        
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(ws_url,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()

# Example usage
if __name__ == "__main__":
    # Initialize the SDK with environment variables for API and private keys.
    sdk = AoriSDK()
    
    # Test connectivity
    connectivity_response = sdk.test_connectivity()
    print(connectivity_response)

    # Retrieve account orders
    account_orders_response = sdk.get_account_orders()
    print(account_orders_response)

    # Retrieve the current orderbook
    orderbook_response = sdk.view_orderbook(chain_id="1", base="insert_eth_address_here", quote="insert_usdc_address_here", side="BUY", limit=50)
    print(orderbook_response)

    # Create a new order
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

    # Take an existing order
    take_order_response = sdk.take_order(
        order_id="123456",
        taker="0x...",
        amount="1000000000000000000",  # Example amount in Wei
        signature="0x..."
    )
    print(take_order_response)

    # Cancel an existing order
    cancel_order_response = sdk.cancel_order(order_id="123456")
    print(cancel_order_response)

    # Request a quote
    quote_response = sdk.request_quote(
        inputToken="0x...",
        outputToken="0x...",
        inputAmount="1000000000000000000",  # Example amount in Wei
        chainId=1
    )
    print(quote_response)
    # Subscribe to orderbook updates
    sdk.subscribe_orderbook()
