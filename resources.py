from dagster import resource, StringSource, Field
import requests
from functools import lru_cache
import hirlite
from toolz import first
import json
import os

@lru_cache(maxsize=30)
def internal_call(url, query, head):
    return requests.get(url, params=json.loads(query), headers=json.loads(head))

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
         
        payload = internal_call(self.endpoint, json.dumps(params), json.dumps(headers))
        return payload.json()
    
class MemStore:
    def __init__(self, path: str):
        self.db = hirlite.Rlite(path)

    def put(self, key: str, values: list):
        return self.db.command("hmset", key, *values)

    def get(self, key: str, val: str):
        item = self.db.command("hmget", key, val)
        return first(item)
    
@resource(
    config_schema={
        "token" : StringSource,
        "endpoint" : Field(str, description="Location to extract FX rates", default_value="https://api.apilayer.com/fixer/latest")
    }
)
def fixer_api(init_context):
    return FixerAPI(init_context.resource_config["token"], init_context.resource_config["endpoint"])


@resource(
    config_schema={
        "path" : Field(str, description="Local file for mem-store", default_value="data/mem/USD.rlite")
    }
)
def mem_store(init_context):
    return MemStore(init_context.resource_config["path"])