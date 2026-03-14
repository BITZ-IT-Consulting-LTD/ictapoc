# --- Production Proxy ---
# This container acts as the SSL-terminating Reverse Proxy
FROM nginx:1.25-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy the specialized proxy configuration (SSL, Buffer tuning, Upstreams)
COPY docker/prod/nginx/default.conf /etc/nginx/conf.d/default.conf

# SSL certificates are mounted via volumes in docker-compose for security and persistence
# No build-stage here, this is a pure lightweight router

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
