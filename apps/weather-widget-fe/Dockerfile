FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
COPY nx.json ./
COPY tsconfig.base.json ./

COPY apps/weather-widget-fe/package*.json ./apps/weather-widget-fe/

RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 4200

CMD ["npx", "nx", "serve", "weather-widget-fe", "--host=0.0.0.0"]
