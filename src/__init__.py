from dagster import Definitions
from .assets import download_currencies
from .resources import fixer_api, mem_store

defs = Definitions(
    assets=[download_currencies],
    resources={
        "fixer_api" : fixer_api.configured(
            {
                "token" : {"env" : "FIXER_API_TOKEN"}
            }
        ),
        "mem_store" : mem_store
    }
) 