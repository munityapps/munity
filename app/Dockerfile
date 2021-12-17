FROM nginx:1.19

WORKDIR /var/www

RUN apt update
RUN apt install -y git npm nodejs
RUN npm install -g yarn

COPY . .

RUN yarn install
RUN yarn build

# COPY ./build /var/www/build
COPY ./server.conf /etc/nginx/conf.d/default.conf
