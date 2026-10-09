FROM node:22-alpine
WORKDIR /app
COPY node_app/package.json node_app/package-lock.json* ./
RUN npm install --omit=dev
COPY node_app/app.js .
EXPOSE 3000
CMD ["npm", "start"]