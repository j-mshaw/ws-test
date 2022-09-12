function getWebSocketServer() {
    if (window.location.host === "j-mshaw.github.io") {
      return "wss://jshaw-ws-test.herokuapp.com:8001.herokuapp.com/";
    } else if (window.location.host === "localhost:8000") {
      return "ws://localhost:8001/";
    } else {
      throw new Error(`Unsupported host: ${window.location.host}`);
    }
  }

  function setup(){
    var chat_area = document.getElementById("chat-area")
    
    var socket = new WebSocket(getWebSocketServer())
    socket.addEventListener("message", (event)=>{
        let message_from_server = event.data
        switch(message_from_server.type){
            case "message_recv":
                var new_node = document.createElement("p")
                new_node.innerText = message_from_server["content"]
                chat_area.appendChild(new_node)
                break
        }
        
        var new_node = document.createElement("p")
        new_node.innerText = event.data
        chat_area.appendChild(new_node)
    });

    var send_button = document.getElementById("send")
    var text_input_area = document.getElementById("message")
    send_button.onclick = () => {
        socket.send(JSON.stringify({"type":"send_msg","content":text_input_area.value}))
        text_input_area.value = ""
    }


}