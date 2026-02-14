# --- Stage 1: Build Stage ---
FROM node:20-alpine AS build-stage

WORKDIR /app

# Enable legacy peer deps for compatibility if needed
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source
COPY ./frontend .

# Build the static application
RUN npm run build

# --- Stage 2: Production Runtime ---
FROM nginx:1.25-alpine-slim

# Copy the build artifacts from the build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Remove default nginx config and replace with our hardened version
RUN rm /etc/nginx/conf.d/default.conf
# Note: The custom config is mounted via volume in docker-compose.prod.yml
# but we can also copy it here for a self-contained image.
COPY docker/prod/nginx/default.conf /etc/nginx/conf.d/default.conf

# Set up permissions for non-root user (Standard Nginx image uses 'nginx' user)
# We ensure the pid file and cache are writable
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /var/log/nginx /usr/share/nginx/html

USER nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
