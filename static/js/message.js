message = "";

let input = document.getElementById("input");
let button = document.getElementById("button");
let response_html = document.getElementById("response");
let sender_address = document.getElementById("sender_address");
let sender_port = document.getElementById("sender_port");
let time = document.getElementById("time");
let database_messages = document.getElementById("database_messages");

function getDatabase() {
  fetch("/database").then(response =>
    response.json().then(json => {
      database_messages.innerText =
        `I've already responded to the following: ` + json.database_messages;
    })
  );
}

getDatabase();

function listenForMessage() {
  message = input.value;
  fetch("/message/?message=" + message).then(response =>
    response.json().then(json => {
      (response_html.innerText = json.message),
        (sender_address.innerText =
          "Sent fromp IP address: " + json.sender_address),
        (sender_port.innerText = "Sent fromp port: " + json.sender_port),
        (time.innerText = json.time);
    })
  );
}

button.addEventListener("click", listenForMessage);
