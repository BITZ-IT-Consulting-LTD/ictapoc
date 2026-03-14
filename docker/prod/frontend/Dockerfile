# --- Stage 1: Build Stage ---
FROM node:20-alpine AS build-stage

WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source and build
COPY ./frontend .
RUN npm run build

# --- Stage 2: Internal Static Server ---
FROM nginx:1.25-alpine-slim

# Copy the build artifacts from the build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Replace default config with the internal frontend config (listens on 8087)
RUN rm /etc/nginx/conf.d/default.conf
COPY docker/prod/nginx/frontend.conf /etc/nginx/conf.d/default.conf

# Set up permissions for non-root user
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /var/log/nginx /usr/share/nginx/html

USER nginx

# Internal port as requested by user
EXPOSE 8087

CMD ["nginx", "-g", "daemon off;"]
