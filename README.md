# Dagster currency downloader

Simple project that uses the Fixer API to download currency prices on a daily basis

```bash
# Create a .env file to store your keys locally
# Add FIXER_API_TOKEN=xxx with your key in the environment

# Install dependencies: pip install dagster dagit hirlite toolz
pip install '.[dev]'

# Run user interface. if using codespaces, a popup will apear to forwarded port 3000
dagit -m src
```

## Explanation

- Project is organized in `assets` and `resources`
- `assets` are files downloaded or created
- `reources` are abstractions to interfaces like file systems, databases, etc. (linked-services)
- 2 resource is defined named: fixer_api and mem_store
- One to download data via `requests`
- The other to store data in memory in sort of `redis` but serverless
- `Definitions` are project workspace declarations, containing assets and resources
- Pressing the button `[Materialize]` will trigger the download of the data and store it locally