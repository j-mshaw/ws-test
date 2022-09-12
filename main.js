function getWebSocketServer() {
    if (window.location.host === "j-mshaw.github.io") {
      return "wss://jshaw-ws-test.herokuapp.com/";
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
        let message_from_server = JSON.parse(event.data)
        console.log(message_from_server)
        switch(message_from_server.type){
            case "recv_msg":
                var new_node = document.createElement("p")
                new_node.innerText = message_from_server.content
                chat_area.appendChild(new_node)
                break
            case "join_resp":
              alert(message_from_server.content)
              break
            case "create_resp":
              alert(message_from_server.content)
              break
        }
    });

    var send_button = document.getElementById("send")
    var text_input_area = document.getElementById("message")
    send_button.onclick = () => {
        socket.send(JSON.stringify({"type":"send_msg","content":text_input_area.value}))
        text_input_area.value = ""
    }

    var join_button = document.getElementById("join")
    join_button.onclick = () => {
      var name_field = document.getElementById("join_input")
      var name = name_field.value
      socket.send(JSON.stringify({"type": "join_req", "name":name}))
    }

    var create_button = document.getElementById("create")
    create_button.onclick = () => {
      var name_field = document.getElementById("create_input")
      var name = name_field.value
      socket.send(JSON.stringify({"type": "create_req", "name":name}))
    }
    
    var leave_button = document.getElementById("leave")
    leave_button.onclick = () => {
      socket.send(JSON.stringify({"type": "leave_req"}))
    }


}