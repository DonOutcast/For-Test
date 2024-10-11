FROM nginx:1.21.3-alpine
ARG NGINX_PORT=80

ENV PORT=${NGINX_PORT}

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE ${PORT}

CMD ["nginx", "-g", "daemon off;"]
