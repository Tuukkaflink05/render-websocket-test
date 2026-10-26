let btn = document.getElementById("sendtoserver");
let list = document.getElementById("list");
let websocket = null;
window.addEventListener("DOMContentLoaded", () => {
  websocket = new WebSocket("ws://localhost:10000/chat");
  //websocket = new WebSocket("wss://websockets-echo-t90c.onrender.com/chat");
  receive(websocket);
  websocket.addEventListener("open", () => send(websocket));
})

function receive(websocket) {
  websocket.addEventListener("message", async (response) => {
    console.log(JSON.parse(response.data));
  })
}

function send(websocket) {
  websocket.send("U:ADMIN");

}

btn.addEventListener("click", () => websocket.send("A:Update list"));

function sendToServer() {
  websocket.send("A:Message from admin");
}