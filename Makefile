down-dev:
	docker compose -f docker-compose.dev.yml down --remove-orphans

up-dev:
	docker compose -f docker-compose.dev.yml up

up-dev-build:
	docker compose -f docker-compose.dev.yml up --build

down-prod:
	docker compose -f docker-compose.prod.yml down --profile prod --remove-orphans

up-prod:
	docker compose -f docker-compose.prod.yml up --profile prod
