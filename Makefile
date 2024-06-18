.PHONY: test

DOCKER_COMPOSE=docker-compose \
	-f tests/integration/neo4j_ephemeral_db/docker-compose.yml
PYTEST=pytest

test: unit_tests integration_tests

unit_tests:
	$(PYTEST) tests/unit

integration_tests:
	@echo "Starting Neo4j container..."
	$(DOCKER_COMPOSE) up -d
	@echo "Running tests..."
	$(PYTEST) tests/integration
	@echo "Tests finished. Tearing down Neo4j container..."
	$(DOCKER_COMPOSE) down

test_env_up:
	@echo "Starting Neo4j container..."
	$(DOCKER_COMPOSE) up -d

lint: lint_corelib lint_tests

lint_corelib:
	pylint corelib

lint_tests:
	pylint tests

