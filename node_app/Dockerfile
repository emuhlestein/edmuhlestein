FROM node:22-alpine
WORKDIR /app

# Install dependencies first (layer is cached unless package*.json change)
COPY node_app/package.json node_app/package-lock.json* ./
RUN npm ci --omit=dev

# Copy the entire application
COPY node_app/ .

EXPOSE 3000
ENTRYPOINT ["./entrypoint.sh"]