
RED 		= \033[0;91m
GREEN 		= \033[0;92m
YELLOW		= \033[0;93m
BLUE		= \033[0;94m
NC			= \033[0m

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

parse: ## Parse an offer
	@echo "$(YELLOW)Enter the offer file location:$(NC)"
	@read offer_file && python3 src/parse_offer.py "$$offer_file"

flake: ## Run flake8 linter
	@echo "$(YELLOW)Running flake8 linter...$(NC)"
	@flake8 src tests

PHONY: help parse flake