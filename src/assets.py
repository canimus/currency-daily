from dagster import asset, Definitions, Field, AssetObservation, DailyPartitionsDefinition
from .resources import fixer_api, mem_store
from datetime import datetime
from functools import partial
from operator import methodcaller
from toolz import compose
from itertools import chain

@asset(
    config_schema={
        "base" : Field(str, description="Currency base", default_value="USD"),
        "symbols" : Field(list, description="Symbols to convert to", default_value=["EUR", "GBP"])
    },
    group_name="fx",
    compute_kind="python",
    required_resource_keys={"fixer_api", "mem_store"},
    partitions_def=DailyPartitionsDefinition(start_date="2022-12-01")
)
def download_currencies(context):

    # Verify if exist in memstore for today
    # today = datetime.today().strftime("%Y-%m-%d")

    today = context.asset_partition_key_for_output()
    context.log.info(f"PARTITION: {today}")

    # Functor for mem-store on today
    _mem = partial(context.resources.mem_store.get, today)

    # Reduce function
    _decode = methodcaller("decode", "utf-8")
    _cast = compose(float, _decode, _mem)

    try:
        rates = {x:_cast(x) for x in context.op_config["symbols"] if x}
        # Found data in memory store
        if rates:
            payload = {
                "success" : True,
                "timestamp" : int(datetime.now().timestamp()),
                "base" : context.op_config["base"],
                "rates" : rates
            }
        
    except AttributeError as e:
        context.log.info("Unable to find key in store")
        
        # Download from internet otherwise
        payload = context.resources.fixer_api.get_latest(
            base=context.op_config["base"],
            symbols=context.op_config["symbols"]
        )

        if payload:
            # Storing in cache
            pairs = list(chain.from_iterable(tuple(payload["rates"].items())))
            context.resources.mem_store.put(today, map(str,pairs))

    context.log_event(
        AssetObservation(asset_key="download_currencies", metadata=payload)
    )

    return payload
    

