FROM node:22-alpine
WORKDIR /app

COPY node_app/package.json node_app/package-lock.json* ./
COPY node_app/entrypoint.sh ./
RUN chmod +x entrypoint.sh

COPY node_app/app.js node_app/db.js ./

EXPOSE 3000
ENTRYPOINT ["./entrypoint.sh"]