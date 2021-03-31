FROM nginx:1.19.0-alpine
  
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY thegreattribblehunt.crt /etc/ssl/certs/thegreattribblehunt.crt
COPY thegreattribblehunt.key /etc/ssl/private/thegreattribblehunt.key
ADD web /usr/share/nginx/html/
ADD web /var/www/html/

