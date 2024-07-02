.PHONY: test

DOCKER_COMPOSE=docker-compose \
	-f tests/integration/neo4j_ephemeral_db/docker-compose.yml
PYTEST=pytest

lint:
	@prospector --profile ../.prospector.yaml $(filter-out $@,$(MAKECMDGOALS))

coverage:
	$(PYTEST) --cov --cov-config ../.coveragerc ./tests/unit

test: unit_tests 
	@echo "NOTE test only runs unit tests."

unit_tests:
	$(PYTEST) tests/unit

test_env_up:
	@echo "Starting Neo4j container..."
	$(DOCKER_COMPOSE) up -d

test_env_down:
	@echo "Stopping Neo4j container..."
	$(DOCKER_COMPOSE) down 

integration_tests:
	@if [ -z "$($(DOCKER_COMPOSE) ps -q neo4j)" ]; then \
		echo "Neo4j container is not running..."; \
		echo "Turn it on with 'make test_env_up'"; \
		exit 1; \
	fi; \

	@echo "Running tests..."
	$(PYTEST) tests/integration
