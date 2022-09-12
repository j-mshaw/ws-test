function setup(){
    var chat_area = document.getElementById("chat-area")
    
    var socket = new WebSocket("ws://localhost:8001")
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