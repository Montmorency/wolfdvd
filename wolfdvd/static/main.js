$(function(){
	console.log("Sanity Check.")
	$("#btn-click").click(function(e) {
		var imdbid =$("imdbid").val()
		console.log(input)
		$.ajax({
			type: "Post"
		  url: $SCRIPT_ROOT + '_modify_db'
		 	data:{
						imdbid: imdbid
			}
	});
});

