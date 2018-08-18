// Prevent holding down key from firing repetedly
var fired = false;
var connStatus = false;

// Get the speed set with slider and update 'speedometer'
var slider = document.getElementById("slider");
var speed = document.getElementById("speed");
var mode = document.getElementById("mode");
var dot = document.getElementById("dot");

speed.innerHTML = slider.value;

slider.oninput = function(){
	speed.innerHTML = this.value;
}

// Stop the robot as soon as button is no longer pressed
window.onload = function(){
	$(".moveButton").mouseup(function() {
		sendMove("stop");
	});

	$("#video").attr("src", "http://" + window.location.hostname +":8081")

	connect();
};

// Add keyboard functionality
window.onkeydown = function (event){
	if (!fired){
		if (event.keyCode == 38){
			sendMove("forward");
		}
		else if (event.keyCode == 40){
			sendMove("backward");
		}
		else if (event.keyCode == 39){
			sendMove("right");
		}
		else if (event.keyCode == 37){
			sendMove("left");
		}
		fired = true;
	}
}

window.onkeyup = function(){
	sendMove("stop");
	fired = false;
}

// Attempt to connect to bot if not already connected
function connect(){
	if (!connStatus){
		getCurrStatus();
	}
}


// Fetch the current mode of the robot and display
function getCurrStatus(){
	fetch("/getStatus")
	.then(function(response){
		return response.json();
	})
	.then(function(jsonResponse){
		connStatus = (jsonResponse.status == "True");

		if (connStatus){
			dot.style.backgroundColor = "#42f483";
			console.log("Robot connected!");
		}else{
			dot.style.backgroundColor = "red";
			console.log("Robot is not connected!");
		}
	});
}


// function to send move data to server
function sendMove(dir) {
	var speed = slider.value;
	var data = {"direction":dir, "speed":speed};

	// ajax the JSON to the server
	$.post({
		type: "POST",
		url: "/move",
		data: JSON.stringify({Data: data}),
	    contentType: "application/json",
	    dataType: "json",
	    success: function(){}
	});

	// stop link reloading the page
	event.preventDefault();
	console.log("Moved " + dir + " at " + speed + "mm/s");
}

/* When the user clicks the button,
toggle between hiding and showing the dropdown content */
function dropDown(){
	document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
	if (!event.target.matches('.dropbtn')) {
	    var myDropdown = document.getElementById("myDropdown");
	    if (myDropdown.classList.contains('show')){
	        myDropdown.classList.remove('show');
	    }
	}
}

// Function that changes robot mode and sends info to server
function changeMode(mode) {
	var data = {"mode":mode};

	// ajax the JSON to the server
	$.post({
		type: "POST",
		url: "/mode",
		data: JSON.stringify({Data: data}),
	    contentType: "application/json",
	    dataType: "json",
	    success: function(){}
	});

	// stop link reloading the page
	event.preventDefault();
	console.log("Changed mode to " + mode);
	this.mode.innerHTML = mode;
}
