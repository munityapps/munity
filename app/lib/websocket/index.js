// Libs
import { io } from 'socket.io-client';
var socket = io("ws://localhost:2000");
socket.on("connect", function () {
    console.log("Connected to socket " + socket.id); // x8WIv7-mJelg7on_ALbx
});
