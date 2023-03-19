# Dagster currency downloader

Simple project that uses the Fixer API to download currency prices on a daily basis

```bash
# Create a .env file to store your keys locally
# Add FIXER_API_TOKEN=xxx with your key in the environment

# Install dependencies: pip install dagster dagit hirlite toolz
pip install '.[dev]'

# Run user interface. if using codespaces, a popup will apear to forwarded port 3000
dagit -f assets.py
```