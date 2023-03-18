
import requests

class FixerAPI:
    def __init__(self, token: str, endpoint : str):
        self.token = token
        self.endpoint = endpoint

    def get_latest(self, base : str = "USD", symbols : list = ["EUR", "GBP"]) -> dict:
        params = {
            "base" : base,
            "symbols" : ",".join(symbols)
        }
        headers = {
            "apikey": self.token
        }
        payload = requests.get(self.endpoint, params=params, headers=headers)
        return payload.json()