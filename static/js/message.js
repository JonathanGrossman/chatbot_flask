message = "";

var input = document.getElementById("input");
var button = document.getElementById("button");

function listenForMessage() {
  message = input.value;
  console.log(message);
}

function respondToMessage() {
  if (input.value === "ddd") {
    console.log(input.value);
  } else {
    console.log("What did you say?");
  }
}

input.addEventListener("change", listenForMessage);

button.addEventListener("click", respondToMessage);
