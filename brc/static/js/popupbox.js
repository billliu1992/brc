function popUp(popUpId, errorMessage)
{
	if(typeof errorMessage !== "undefined")
	{
		$("#" + popUpId + " .notif-error").text(errorMessage);
	}

	var windowWidth = $(document).width();
	var windowHeight = $(document).height();
	var popUpWidth = $("#" + popUpId).width();
	var popUpHeight = $("#" + popUpId).height();

	var bgObj = createBackground(windowWidth, windowHeight);
	$("#" + popUpId).show();
	$("#" + popUpId).css("left", windowWidth/2 - popUpWidth/2);
	$("#" + popUpId).css("top", windowHeight/2 - popUpHeight/2);
	
	bgObj.click(function()
		{
			closePopUp(popUpId);
			$("#" + popUpId + " .notif-error").text("");
		});
		
	$(".popup-close").click(function()
		{
			closePopUp(popUpId);
			$("#" + popUpId + " .notif-error").text("");
		});
}

function createBackground(width, height)
{
	var backgroundObj = $("<div class='popup-background'></div>");
	
	backgroundObj.css("width", width);
	backgroundObj.css("height", height);
	
	backgroundObj.insertBefore(".popup-box");
	
	return backgroundObj;
}

function closePopUp(popUpId)
{
	$("#" + popUpId).hide();
	$(".popup-background").remove();
}
