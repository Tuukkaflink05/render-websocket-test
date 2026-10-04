let websocket = null;
window.addEventListener("DOMContentLoaded", () => {
  websocket = new WebSocket("ws://localhost:10000/chat");
  receive(websocket);
  websocket.addEventListener("open", () => send(websocket));
})

function receive(websocket) {
  websocket.addEventListener("message", ({ data }) => {
    console.log(data);
  })
}

function send(websocket) {
  websocket.send("U:ADMIN");

}


function sendToServer() {
  websocket.send("A:Message from admin");
}