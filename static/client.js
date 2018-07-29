
// Get the speed set with slider and update 'speedometer'
var slider = document.getElementById("slider");
var speed = document.getElementById("speed");
var mode = document.getElementById("mode");

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

	getCurrMode();
};

// Add keyboard functionality
window.onkeydown = function (event){
	if (event.keyCode == 38)
{		sendMove("forward");
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
}

window.onkeyup = function(){
	sendMove("stop");
}

/* Fetch the current mode of the robot and display
function getCurrMode(){
	fetch("/getMode")
	.then(function(response){
		return response.json();
	})
	.then(function(jsonResponse){
		mode.innerHTML = jsonResponse.mode;
	});
}
*/

// function to send move data to server
function sendMove(dir) {
	speed = slider.value;
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
	//getCurrMode();
}
