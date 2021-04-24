// Libs
import { io } from 'socket.io-client';

const socket = io("ws://localhost:2000");
socket.on("connect", () => {
  console.log(socket.id); // x8WIv7-mJelg7on_ALbx
});
