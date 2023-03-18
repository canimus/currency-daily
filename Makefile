clean: # Remove workspace files
	@find . -name "__pycache__" -exec rm -rf {} + 
	@rm -rf ./.pytest_cache
	@rm -rf ./htmlcov
	@rm -rf dist/
	@rm -rf build/
	@rm -rf __blobstorage__
	@rm -rf .mypy_cache
	@rm -rf .coverage