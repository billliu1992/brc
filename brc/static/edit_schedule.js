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
	
	$("#day_num_"+entry_num).attr("style", "visibility:hidden");
	$("#reading_"+entry_num).attr("style", "visibility:hidden");
	
	$("#display_day_num_"+entry_num).attr("style", "visibility:visible");
	$("#display_reading_"+entry_num).attr("style", "visibility:visible");
}

function hideAllInputShowDisplay()
{
	var total_entries_num = $("#entries_num").val()
	console.log(total_entries_num);
	for(var i = 0; i < total_entries_num; i++)
	{
		hideInputShowDisplay(i);
	}
}

function showInputHideDisplay(entry_num)
{
	var new_day_num = $("#display_day_num_"+entry_num).text();
	var new_reading = $("#display_reading_"+entry_num).text();

	$("#day_num_"+entry_num).val(new_day_num);
	$("#reading_"+entry_num).val(new_reading);

	$("#day_num_"+entry_num).attr("style", "visibility:visible");
	$("#reading_"+entry_num).attr("style", "visibility:visible");
	
	$("#display_day_num_"+entry_num).attr("style", "visibility:hidden");
	$("#display_reading_"+entry_num).attr("style", "visibility:hidden");
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
	for(var i = 0; i < total_entries_num; i++)
	{
		registerClick(i)
	}
}

function registerClick(entry_num)
{
	$("#row_"+entry_num).click(function() {clickOnEntry(entry_num)});
	console.log("REGISTERING FOR: " + "#row_"+entry_num)
}

function addEntry()
{
	entry_num = parseInt($("#entries_num").val());
	
	//Add the html to the page
	var new_entry_html = "<tr id=\"row_" + entry_num + "\">" +
							"<td>" +
								"<label for=\"day_num_" + entry_num + "\" id=\"label_day_num_" + entry_num + "\">Day Number: </label>" +
								"<input type=\"text\" name=\"day_num_" + entry_num + "\" id=\"day_num_" + entry_num + "\" class=\"entry_input\" size=\"3\"/>" +
								"<p id=\"display_day_num_" + entry_num + "\" class=\"entry_display\"></p>" + 
							"</td>" +
							"<td>" +
								"<label for=\"reading_" + entry_num + "\" id=\"label_reading_" + entry_num + "\">Reading: </label>" + 
								"<input type=\"text\" name=\"reading_" + entry_num + "\" id=\"reading_" + entry_num + "\" class=\"entry_input\"/>" + 
								"<p id=\"display_reading_" + entry_num + "\" class=\"entry_display\"></p>" + 
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
