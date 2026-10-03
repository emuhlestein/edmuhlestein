FROM node:22-alpine
WORKDIR /app
COPY node/package.json node/package-lock.json* ./
RUN npm install --omit=dev
COPY node/server.js .
EXPOSE 2567
CMD ["npm", "start"]
