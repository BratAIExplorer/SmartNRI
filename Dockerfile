FROM nginx:1.27-alpine

# Copy the SmartNRI frontend
COPY frontend/index.html /usr/share/nginx/html/index.html

# Custom Nginx config for security headers
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose internal port
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost/ > /dev/null || exit 1
