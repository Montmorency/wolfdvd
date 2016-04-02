$(function() {
  console.log("whee!")
	$("#btn-click").click(function() {
		var input = $("input").val()
		console.log("You Clicked a Button!")
		console.log(input)
		console.log($WOLFLOC)
	});
});
