FROM node:22-alpine
WORKDIR /app

COPY node_app/package.json node_app/package-lock.json* ./
RUN npm install

COPY node_app/app.js node_app/db.js ./

RUN npm prune --omit=dev

EXPOSE 3000
CMD ["npm", "start"]