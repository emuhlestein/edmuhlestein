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

### Up Dev Local for node_app (could be any service)
docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev up -d --build node_app

### Down Dev Local
docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev down --remove-orphans

### Restart node_app serivce
docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev restart node_app

### Show log for node_app service
docker --context default compose -f docker-compose.dev.yml  --env-file .env.dev logs -f node_app

### Show which containers are running
docker --context default compose -f docker-compose.dev.yml ps

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


### Cookie
- **secure**  
	- true — the browser will only attach the cookie to HTTPS requests.
	- false — the cookie is sent over both HTTP and HTTPS.  
	In production (behind nginx with HTTPS) you want true. In local development on plain HTTP you need false, otherwise the browser never sends the cookie and sessions never work.  
	Cookie is encrypted in transit (because it only travels over HTTPS).  
- **httpOnly**
	- true — the cookie is not accessible from JavaScript (document.cookie cannot see it).  
	- This is the normal setting. It reduces the damage if an XSS bug exists in your frontend, because an attacker cannot steal the session cookie with script.  
	Cookie is hidden from client-side script.  
- **sameSite**  
	Controls when the browser includes the cookie on cross-site requests.  
	- "lax" (recommended default) — the cookie is sent on top-level navigations (clicking a link to your site) but not on cross-site AJAX/fetch/form posts. Good balance of security and usability.  
	- "strict" — cookie is only sent when the request originates from the same site. Slightly safer, but can break some login-return flows.  
	- "none" — cookie is always sent (requires secure: true). Needed only for cross-site embedding (rare).  
	Cookie is mostly limited to same-site requests.  

### app.set("trust proxy", 1);  

nginx terminates HTTPS and forwards the request to your Node container over plain HTTP. Without trust proxy, Express thinks every request is HTTP, so a secure: true cookie is never set and the browser never receives a session.  
trust proxy: 1 tells Express to look at the X-Forwarded-Proto header that nginx already sends and treat the original request as HTTPS when that header says https.Place the line anywhere before app.use(session(...)) and it will take effect.