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