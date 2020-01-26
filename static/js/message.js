function listenForMessage() {
  console.log("message");
}

var button = document.getElementById("button");
button.addEventListener("click", listenForMessage);
