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