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


**To show all CLI commands**
docker compose -f docker-compose.dev.yml run --rm cli

docker compose -f docker-compose.dev.yml build cli

