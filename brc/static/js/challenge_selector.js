function ScheduleSelector(filterField, resultsDiv, allSchedulesJson) {
	this.filterField = filterField;
	this.resultsDiv = resultsDiv;
	this.scheduleObjs = allSchedulesJson;
	
	this.resultEntryClass = "schedule-result-entry";
	this.selectedEntryClass = "schedule-result-selected-entry";
	this.selectedInputId = "schedule-result-selected";
	
	this.initSelector();
}

ScheduleSelector.prototype = {
	/**
	 *  Create all the HTML elements
	 */
	initSelector : function() {
		this.doFilter();
		
		selectorObj = this;
		
		$(this.filterField).keydown(function() {
			selectorObj.doFilter();
		});
		
		$(this.filterField).keyup(function() {
			selectorObj.doFilter();
		});
	},
	
	doFilter : function() {
		var filterBy = $(this.filterField).val().toLowerCase();
		
		var filteredEntries = [];
		
		for(i = 0; i < this.scheduleObjs.length; i++) {
			if(this.scheduleObjs[i]['name'].toLowerCase().indexOf(filterBy) > -1) {
				filteredEntries.push(this.scheduleObjs[i]);	
			}
		}
		
		this.createResultsHtml(filteredEntries);
		
	},
	
	createResultsHtml : function(entries) {
		$(this.resultsDiv).html("");
		$(this.resultsDiv).append($("<input type='hidden' id='" + this.selectedInputId + "' />"));
		for(i = 0; i < entries.length; i++) {
			entryHtmlObj = $("<div class='" + this.resultEntryClass + "' entrypk='" + this.scheduleObjs[i]['pk'] + "'></div>");
			entryHtmlObj.append($("<span class='entry-name'>" + this.scheduleObjs[i]['name'] + "</span>"));
			entryHtmlObj.append($("<span class='entry-dates'>" + this.scheduleObjs[i]['date'] + "</span>"));
			
			$(this.resultsDiv).append(entryHtmlObj);
		}
		
		$("." + this.resultEntryClass).click(function(event) {
			$("#" + this.selectedInputId).val($(this).attr("entrypk"));
			$(this).addClass(this.selectedEntryClass);
			
			console.log("YOU CLICKED ME: " + $(this).attr("entrypk"));
		});
	}
	
	
}
