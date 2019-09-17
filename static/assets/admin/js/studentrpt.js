
function hideStudent() {
    // Declare all variables
  var i, tabcontent;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

}


function openStudent(evt, name) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the link that opened the tab
  document.getElementById(name).style.display = "block";
  evt.currentTarget.className += " active";
  //courtesy of w3schools
}

function hideAlert(){
    // Declare all variables
  var i, alert;

  // Get all elements with class="tabcontent" and hide them
  alert = document.getElementsByClassName("alert");
  for (i = 0; i < alert.length; i++) {
    alert[i].style.display = "none";
  }

}

function showAlert() {
  // Declare all variables
  var i, alert;

  // Get all elements with class="tabcontent" and hide them
  alert = document.getElementsByClassName("alert");
  for (i = 0; i < alert.length; i++) {
    alert[i].style.display = "none";
  }
}