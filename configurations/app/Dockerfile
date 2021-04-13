FROM nginx:1.19

WORKDIR /var/www

RUN apt update
RUN apt install -y git npm nodejs yarn

COPY ./app/build /var/www/build
COPY ./configurations/app/server.conf /etc/nginx/conf.d/default.conf