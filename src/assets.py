from dagster import asset, Definitions
import requests

@asset
def download_currencies(context):
    pass