FROM node:18-alpine
WORKDIR /app

COPY backend/package.json backend/package-lock.json ./backend/
RUN cd backend && npm install

COPY backend ./backend
COPY frontend ./frontend

WORKDIR /app/backend
CMD ["node", "server.js"]
