message = "";

let input = document.getElementById("input");
let button = document.getElementById("button");
let response_html = document.getElementById("response");
let response_origin = document.getElementById("response_origin");
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
  let sender_details_wrapper = document.getElementById(
    "sender_details_wrapper"
  );
  sender_details_wrapper.classList.remove("hidden");
  sender_details_wrapper.classList.add("sender_details_wrapper");
  let response_div = document.getElementById("response");
  response_div.classList.remove("hidden");
  response_div.classList.add("response");
  message = input.value;
  fetch("/message/?message=" + message).then(response =>
    response.json().then(json => {
      (response_html.innerText = json.message),
        (response_origin.innerText = json.message_origin),
        (sender_address.innerText =
          "Sent from IP address: " + json.sender_address),
        (sender_port.innerText = "Sent from port: " + json.sender_port),
        (time.innerText = json.time);
    })
  );
}

button.addEventListener("click", listenForMessage);
