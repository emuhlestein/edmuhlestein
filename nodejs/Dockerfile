FROM node:slim

WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY app/ .

ENTRYPOINT ["node", "app.js"]