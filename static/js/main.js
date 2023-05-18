function validate() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  
  if (username == "" || password == "") {
    alert("Please fill in all fields.");
    return false;
  }
  // else if (username.length < 4) {
  //   alert("Username must be at least 4 characters long.");
  //   return false;
  // }
  // else if (password.length < 6) {
  //   alert("Password must be at least 6 characters long.");
  //   return false;
  // }
  // else {
  //   alert("Login successful!");
  //   return true;
  // }
}

