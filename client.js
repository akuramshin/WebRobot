function sendMove(dir) {

	speed = 5;
	var data = {"direction":dir, "speed":speed};

	// ajax the JSON to the server
	$.post({
		type: "POST",
		url: "/move",
		data: JSON.stringify({Data: data}),
	    contentType: "application/json",
	    dataType: "json",
	    success: function(){console.log("sent");}
	});

	// stop link reloading the page
	event.preventDefault();
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
	console.log("Changed mode to " + mode);
}
