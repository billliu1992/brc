/* edit_schedule.js
 * JavaScript for the edit schedule page
 * Uses JQuery
 */
 

function hideInput(entry_num)
{
	$(".entry_input").attr("style", "display:none")
}

function showDisplay(entry_num)
{
	$("#day_num_"+entry_num).val()
	$("#day_num_"+entry_num)
}

function addEntry(entry_num)
{
	var new_entry_html = "<tr>" +
							"<td>" +
								"<label for=\"day_num\">Day Number:</label>" +
								"<input type=\"text\" name=\"day_num_" + entry_num + "\" id=\"day_num_" + entry_num + "\" class=\"entry_input\" size=3/>" +
								"<p id=\"display_day_num_" + entry_num + "\" class=\"entry_display\" style=\"display:none\"></p>
							"</td>" +
							"<td>" +
								"<label for=\"date\">Reading:</label>"
								"<input type=\"text\" name=\"reading_" + entry_num + "\" id=\"reading_" + entry_num + "\" class=\"entry_input\"/>"
								"<p id=\"display_reading_" + entry_num + "\" class=\"entry_display\" style=\"display:none\"></p>
							"</td>" +
						"</tr>"
	$("#entry_list").find("table").append(new_entry_html)
}
