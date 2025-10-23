#!/bin/sh
set -e

# Default to port 8080 if PORT is not set
PORT=${PORT:-8080}

# Replace $PORT in nginx config template
envsubst '${PORT}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Start nginx
exec nginx -g 'daemon off;'
