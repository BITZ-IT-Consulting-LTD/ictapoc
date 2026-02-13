# Build Stage
FROM node:18-alpine as build-stage
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY ./frontend .
RUN npm run build

# Production Stage to serve with Nginx
FROM nginx:alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config
COPY docker/prod/nginx/default.conf /etc/nginx/conf.d/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
