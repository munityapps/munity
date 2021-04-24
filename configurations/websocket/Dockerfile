FROM node:15.14.0-buster-slim

RUN apt update
RUN apt install -y yarn

RUN mkdir -p /home/node/app

COPY ./websocket/package.json /home/node/app
WORKDIR /home/node/app

RUN yarn install

COPY ./websocket/ /home/node/app
