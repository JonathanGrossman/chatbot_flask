message = "";

let input = document.getElementById("input");
let button = document.getElementById("button");
let response = document.getElementById("response");

function listenForMessage() {
  message = input.value;
  console.log(message);
}

function respondToMessage() {
  response.innerText = "What did you say?";
}

input.addEventListener("change", listenForMessage);
button.addEventListener("click", respondToMessage);
