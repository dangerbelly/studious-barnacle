
var _g;

function showDiv(){

			$("#myId").removeClass('hidden')
			localStorage.setItem('show','true');
		}
function sndForm(){
	gradeupload = document.getElementById("gradeupload");
	_g = gradeupload.options[gradeupload.selectedIndex].value;

}

$(document).ready(function() {

	console.log("ready!");

	//localStorage.removeItem('show','true');

	$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        //var form_data = new FormData($('#gradeupload')[0]);
        console.log($("#gradeupload"))
        //var test = ['this text']
        //form_data.append('data', $("gradeupload")[0]);
        $.ajax({
            type: 'POST',
            url: '/test2',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(data) {
                console.log('Success!');
            },
        });
    });
});


	$("form").on("submit", function() {
		console.log("the form has been submitted")

		var valueOne = $('input[name="file"]').val()

		localStorage.setItem('show','true');

		sndForm();

		console.log(_g);

		console.log(valueOne);

		$.ajax({
			type: "POST",
			url: "/test",
			data: {"first":5,"grade_value":_g,"file":valueOne},
			//$("#results").html(results)
			success: function(results) {
				console.log(results);
				$("#total_students").html(results.total_students)
				$("#results").html(results.data1)
				$("#school_number").html(results.school_number)
				$("#schools").html(results.schools)

				var show = localStorage.getItem('show');
		
		if (show ==='true'){
			$("#myId").show()
		}
		console.log(show);
    				      		    							
			},
			error: function(error) {
				console.log(error);
			}
		});


	});

		var show = localStorage.getItem('show');
		
		if (show ==='true'){
			$("#myId").show()
		}
		console.log(show);





});

	$(".form").on("submit", function(e){

	e.preventDefault();
	$(this).tab('show');
	})
	.on("click", "span", function(){
		var anchor = $(this).siblings('a');
		$(anchor.att('href')).remove();
		$(this).parent().remove();
        $(".nav-tabs li").children('a').first().click();
    });

    $('.add-contact').click(function(e) {
        e.preventDefault();
        var id = $(".nav-tabs").children().length; //think about it ;)
        $(this).closest('li').before('<li><a href="#contact_'+id+'">New Tab</a><span>x</span></li>');         
        $('.tab-content').append('<div class="tab-pane" id="contact_'+id+'">Contact Form: New Contact '+id+'</div>');
	});


