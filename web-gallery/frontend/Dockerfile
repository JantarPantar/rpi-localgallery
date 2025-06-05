FROM nginx:alpine
FROM node:alpine

WORKDIR /app
COPY . .

RUN npm install -g http-server

CMD ["http-server", "-p", "80"]
COPY index.html /usr/share/nginx/html/index.html
