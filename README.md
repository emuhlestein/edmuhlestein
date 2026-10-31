This is a FastAPI web application. This is to help me learn Python.  

It uses Docker.
**To run the web app in development:**  

 docker compose -f docker-compose.dev.yml up [-d] [--build] [--no-cache]

 **To bring it down in development:**  

 docker compose -f docker-compose.dev.yml down --remove-orphans  

 **To run the web app in production:**  

 docker compose -f docker-compose.prod.yml up [-d] [--build] [--no-cache] --profile prod  

**To bring it down in production:**  

docker compose -f docker-compose.prod.yml down --profile prod --remove-orphans  

**One-time manual cert issuance (e.g., initial setup in prod):**  

docker compose -f docker-compose.prod.yml run --rm certbot certonly --webroot -w /var/www/certbot -d example.com

### To show all CLI commands
docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev run --rm cli

docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev run --rm cli dump-users

**example**
docker compose -f docker-compose.dev.yml run --rm cli show-env

docker compose -f docker-compose.dev.yml build cli

docker compose -f docker-compose.dev.yml run fastapi bash

### Up Dev Local
docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev up -d --build

### Down Dev Local
docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev down --remove-orphans

### Restart node_app serivce
docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev restart node_app

### Show log for node_app service
docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev logs -f node_app

**Up dev VM**
	docker --context remote-prod compose -f docker-compose.dev.yml  --env-file .env.dev up -d --build

**Down Dev VM**
	docker --context remote-prod compose -f docker-compose.dev.yml  --env-file .env.dev down --remove-orphans


**Up Prod Local**
	docker --context default compose -f docker-compose.prod.yml  --env-file .env.prod up -d --build

### Down Prod Local
	docker --context default compose -f docker-compose.prod.yml  --env-file .env.prod down --remove-orphans

**Up Prod VM**
	docker --context remote-prod compose -f docker-compose.prod.yml  --env-file .env.prod up -d --build

**Down Prod VM**
	docker --context remote-prod compose -f docker-compose.prod.yml  --env-file .env.prod down --remove-orphans

### To run a sql script on postgres
docker --context default compose -f docker-compose.dev.yml exec -T postgres psql -U postgres -d appdb -f - < 1.0.sql

** Network **
Remote context for VM: ssh://ed@192.168.1.19
To access VM: ssh ed@192.168.1.19

WSL2 Unbuntu is running on a different IP from my laptop.
