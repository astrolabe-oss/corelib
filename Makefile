.PHONY: test

DOCKER_COMPOSE=docker-compose \
	-f tests/integration/neo4j_ephemeral_db/docker-compose.yml
PYTEST=pytest

test:
	@echo "Starting Neo4j container..."
	$(DOCKER_COMPOSE) up -d
	@echo "Running tests..."
	$(PYTEST)
	@echo "Tests finished. Tearing down Neo4j container..."
	$(DOCKER_COMPOSE) down

test_env_up:
	@echo "Starting Neo4j container..."
	$(DOCKER_COMPOSE) up -d

lint:
	pylint corelib
	pylint tests
