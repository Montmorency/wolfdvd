$(function(){
	console.log("Sanity Check.")
	console.log($SCRIPT_ROOT)
	console.log($WOLFLOC)
	$("#btn-click").click(function() {
		var imdbid =$("#imdbid").val();
		console.log(imdbid);
		$.ajax({
		  url: "/_modify_db",
			data: {'hello':'world', 'hello': 'world!'}
			dataType:'json'
			type: "POST",
    	success: function(data) {
                console.log(data);
								timeout 10000
            },
            error: function(error) {
                console.log(error);
            }
		});
	});
});
