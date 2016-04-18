$(function() {
  console.log("whee!")
	$("#btn-click").click(function() {
		var input = $("input").val()
		$.ajax({
			method : "POST",
			url  : '/_modify_db',
			data : {imdbid : input, wolfloc : $WOLFLOC }
		}).done(function(msg) {
			alert("Title ID updated.");
		});
	});
});
