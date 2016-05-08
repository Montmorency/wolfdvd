$( document ).ready(function() {
  console.log("whee! Replace this with a server side IMDB query so we can load the search dynamically.");
});

// This is shorthand for $(document).ready(function() {...});
$(function() {
	$("#btn-click").click(function() {
		var input = $("input").val()
		$.ajax({
			method : "POST",
			url  : '/_modify_db',
			data : {imdbid : input, wolfloc : $WOLFLOC },
			success: function(response){
			window.location.href = response;}
		}).done(function(data) {
			alert("Title ID updated.");
		});
	});
});
