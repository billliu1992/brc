/* edit_schedule.js
 * JavaScript for the edit schedule page
 * Uses JQuery
 */
 

function hideInputShowDisplay(entry_num)
{
	var new_day_num = $("#day_num_"+entry_num).val();
	var new_reading = $("#reading_"+entry_num).val();

	$("#display_day_num_"+entry_num).text(new_day_num);
	$("#display_reading_"+entry_num).text(new_reading);
	
	$("#day_num_"+entry_num).attr("style", "display:none");
	$("#reading_"+entry_num).attr("style", "display:none");
	
	$("#display_day_num_"+entry_num).attr("style", "display:inline");
	$("#display_reading_"+entry_num).attr("style", "display:inline");
}

function hideAllInputShowDisplay()
{
	var total_entries_num = $("#entries_num").val()
	for(var i = 1; i <= total_entries_num; i++)
	{
		hideInputShowDisplay(i-1);
	}
}

function showInputHideDisplay(entry_num)
{
	var new_day_num = $("#display_day_num_"+entry_num).text();
	var new_reading = $("#display_reading_"+entry_num).text();

	$("#day_num_"+entry_num).val(new_day_num);
	$("#reading_"+entry_num).val(new_reading);

	$("#day_num_"+entry_num).attr("style", "display:inline");
	$("#reading_"+entry_num).attr("style", "display:inline");
	
	$("#display_day_num_"+entry_num).attr("style", "display:none");
	$("#display_reading_"+entry_num).attr("style", "display:none");
}

function clickOnEntry(entry_num)
{
	hideAllInputShowDisplay()
	showInputHideDisplay(entry_num)
}

/*
 * Registers all the display_day_num and display_reading to show the text field when
 * clicked on
 */
function registerClicks(total_entries_num)
{
	for(var i = 1; i <= total_entries_num; i++)
	{
		registerClick(i-1)
	}
}

function registerClick(entry_num)
{
	console.log("REGISTERING: " + entry_num)
	$("#row_"+entry_num).click(function() {clickOnEntry(entry_num)});
}

function addEntry()
{
	entry_num = parseInt($("#entries_num").val());
	
	//Add the html to the page
	var new_entry_html = "<tr id=\"row_" + entry_num + "\">" +
							"<td style=\"display:table-cell\">" +
								"<label for=\"day_num_" + entry_num + "\" id=\"label_day_num_" + entry_num + "\">Day Number: </label>" +
							"</td>" +
							"<td style=\"display:table-cell; width:35px\">" +
								"<span id=\"display_day_num_" + entry_num + "\" class=\"entry_display\"></span>" + 
								"<input type=\"text\" name=\"day_num_" + entry_num + "\" id=\"day_num_" + entry_num + "\" class=\"entry_input\" size=\"1\"/>" +
							"</td>" + 
							"<td style=\"display:table-cell\">" +
								"<label for=\"reading_" + entry_num + "\" id=\"label_reading_" + entry_num + "\">Reading: </label>" + 
							"</td>" +
							"<td style=\"display:table-cell; width:100px\">" +
								"<span id=\"display_reading_" + entry_num + "\" class=\"entry_display\"></span>" + 
								"<input type=\"text\" name=\"reading_" + entry_num + "\" id=\"reading_" + entry_num + "\" class=\"entry_input\"/>" + 
							"</td>" +
						"</tr>"
	$("#entries_table").append(new_entry_html)
	
	//increase the number of entries
	$("#entries_num").val(entry_num+1)
	
	registerClick(entry_num)
	
	//animation
	$("#row_"+entry_num).hide()
	$("#row_"+entry_num).fadeIn()
	
	
	hideAllInputShowDisplay()
}
