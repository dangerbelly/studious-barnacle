$(document).ready(function() {

	console.log("ready!");

	$("form").on("submit", function() {
		console.log("the form has been submitted")

		var valueOne = $('input[name="number-one"]').val()

		console.log(valueOne)

		$.ajax({
			type: "POST",
			url: "/index",
			data: {first:valueOne}

		});
	});
	
});
