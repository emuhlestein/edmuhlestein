.PHONY: down-dev up-dev up-dev-build \
        down-prod up-prod \
        up-prod-local down-prod-local \
        up-prod-remote down-prod-remote

COMPOSE_DEV  := docker compose -f docker-compose.dev.yml --env-file .env.dev
COMPOSE_PROD := docker compose -f docker-compose.prod.yml --env-file .env.prod

down-dev:
	$(COMPOSE_DEV) down --remove-orphans

up-dev:
	$(COMPOSE_DEV) up -d

up-dev-build:
	$(COMPOSE_DEV) up -d --build

down-prod:
	$(COMPOSE_PROD) down --remove-orphans

up-prod:
	$(COMPOSE_PROD) up

# --- prod pinned to an engine ---
up-prod-local:
	docker --context default compose -f docker-compose.prod.yml  up -d --build

down-prod-local:
	docker --context default compose -f docker-compose.prod.yml  down --remove-orphans

up-prod-remote:
	docker --context remote-prod compose -f docker-compose.prod.yml  up -d --build

down-prod-remote:
	docker --context remote-prod compose -f docker-compose.prod.yml  down --remove-orphans

