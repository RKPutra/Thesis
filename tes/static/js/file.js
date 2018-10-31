$(document).ready(function () {
	$("input[class='form-check-input']").change(function () {
		$("input[class='form-check-input']").removeAttr( "required" )
		var maxAllowed = 3;
		var cnt = $("input[class='form-check-input']:checked").length;
		if (cnt > maxAllowed)
		{
			$(this).prop("checked", "");
			alert('Select maximum ' + maxAllowed + ' Class!');
		}
	});
});
