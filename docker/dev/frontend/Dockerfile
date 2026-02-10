# frontend/docker/dev/frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY frontend/package.json /app/
COPY frontend/package-lock.json /app/

RUN npm install

COPY ./frontend /app/

EXPOSE 5173

CMD ["npm", "run", "dev"]
