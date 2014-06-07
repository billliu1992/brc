function TextConfirm(identifier, confirmCallback) {
	this.identifier = identifier;
	this.confirmCallback = confirmCallback;
	
	this.initializeConfirm();
}

TextConfirm.prototype = {
	initializeConfirm : function() {
		that = this;
		
		$(this.identifier).click(function() {
			that.putPrompt();
		});
	},
	
	putPrompt : function() {
	
		that = this;
	
		putHtml = "<span id='text-conf'>Confirm? <span id='text-conf-no'>No</span> <span id='text-conf-yes'>Yes</span>"
		
		$(putHtml).insertAfter(this.identifier);
		$(this.identifier).hide();
		
		$('#text-conf-no').click(function() {
			$(that.identifier).show();
			that.deletePrompt();
		});
		
		$('#text-conf-yes').click(function() {
			$(that.identifier).show();
			that.deletePrompt();
			
			that.confirmCallback();
		});
	},
	
	deletePrompt : function() {
		$('#text-conf').remove();
	}
}
