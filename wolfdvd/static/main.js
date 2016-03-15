$(function(){
	console.log("Sanity Check.")
	$("#btn-click").click(function(e) {
		var input =$("input").val()
		console.log(input)
		$.ajax({
			url  : '/modify_title/',
			data :$('form').serialize(),
			type : 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
	});
});

