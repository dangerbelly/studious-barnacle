$(document).ready(function() {

	console.log("ready!");

	$("form").on("submit", function() {
		console.log("the form has been submitted")

		var valueOne = $('input[name="file"]').val()

		console.log(valueOne)

		$.ajax({
			type: "POST",
			url: "/test",
			data: {first:5},
			//$("#results").html(results)
			success: function(results) {
				console.log(results);
				$("#total_students").html(results.total_students)
				$("#results").html(results.data1)
				$("#school_number").html(results.school_number)
				$("#schools").html(results.schools)
			},
			error: function(error) {
				console.log(error);
			}
		});

	});
	
});
