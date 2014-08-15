function ScheduleSelector(filterField, resultsDiv, allSchedulesJson) {
	this.filterField = filterField;
	this.resultsDiv = resultsDiv;
	this.scheduleObjs = allSchedulesJson;
	
	this.resultEntryClass = "schedule-result-entry";
	this.selectedEntryClass = "schedule-result-selected-entry";
	this.selectedInputId = "schedule-result-selected";
	this.moreButtonId = "schedule-result-more";
	
	this.currentEntries = [];
	
	this.currentPageNum = 0;
	this.numPerPage = 20;
	
	this.initSelector();
}

ScheduleSelector.prototype = {
	/**
	 *  Create all the HTML elements
	 */
	initSelector : function() {
		this.doFilter();
		
		selectorObj = this;
		
		$("#" + this.filterField).keydown(function() {
			selectorObj.doFilter();
		});
		
		$("#" + this.filterField).keyup(function() {
			selectorObj.doFilter();
		});
	},
	
	doFilter : function() {
		var filterBy = $("#" + this.filterField).val().toLowerCase();
		
		var filteredEntries = [];
		
		for(i = 0; i < this.scheduleObjs.length; i++) {
			if(this.scheduleObjs[i]['name'].toLowerCase().indexOf(filterBy) > -1) {
				filteredEntries.push(this.scheduleObjs[i]);	
			}
		}
		
		this.currentEntries = filteredEntries;
		
		this.createResultsHtml();
		
	},
	
	createResultsHtml : function() {
		$("#" + this.resultsDiv).html("");
		
		for(i = 0; i < Math.min(this.currentEntries.length, this.numPerPage); i++) {
			var entryHtmlObj = $("<div class='" + this.resultEntryClass + "' entrypk='" + this.scheduleObjs[i]['pk'] + "'></div>");
			entryHtmlObj.append($("<span class='entry-name'>" + this.currentEntries[i]['name'] + "</span>"));
			entryHtmlObj.append($("<span class='entry-date'>" + this.currentEntries[i]['date'] + "</span>"));
			
			$("#" + this.resultsDiv).append(entryHtmlObj);
		}
		
		var moreButton = $("<div id='" + this.moreButtonId + "'>Show more results</div>");
		
		$("#" + this.resultsDiv).append(moreButton);
		
		this.currentPageNum = 0;
		this.doMoreButtonVisibility();
		
		thisSelector = this;
		
		$("." + this.resultEntryClass).click(function(event) {
			$("#" + thisSelector.selectedInputId).val($(this).attr("entrypk"));
			$(this).addClass(thisSelector.selectedEntryClass);
		});
		
		$("#" + this.moreButtonId).click(function() {
			thisSelector.showMoreResults();
		});
	},
	
	doMoreButtonVisibility : function() {
		if((this.currentPageNum + 1) * this.numPerPage < this.currentEntries.length) {
			$("#" + this.moreButtonId).show();
		}
		else {
			$("#" + this.moreButtonId).hide();
		}
	},
	
	showMoreResults : function() {
		this.currentPageNum += 1;
		
		for(i = this.currentPageNum * this.numPerPage; i < Math.min(this.currentEntries.length, (this.currentPageNum + 1) * this.numPerPage); i++) {
			var entryHtmlObj = $("<div class='" + this.resultEntryClass + "' entrypk='" + this.scheduleObjs[i]['pk'] + "'></div>");
			entryHtmlObj.append($("<span class='entry-name'>" + this.currentEntries[i]['name'] + "</span>"));
			entryHtmlObj.append($("<span class='entry-date'>" + this.currentEntries[i]['date'] + "</span>"));
			
			$("#" + this.moreButtonId).append(entryHtmlObj);
		}
		
		this.doMoreButtonVisibility();
		
	}
}
