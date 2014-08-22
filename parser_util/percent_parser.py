def parse_percent(decimal, verbose = False):
	"""
	Turns the decimal representation to a percentage string
	"""
	percent_str = str(decimal).split(".")[1]
	
	if(verbose):
		#So you don't get 0.%, this adds a 0 so you get 0.0%
		if(percent_str[2:4] == ''):
			decimal_portion = "0"
		else:
			decimal_portion = percent_str[2:4]
		
		return percent_str[:2] + "." + decimal_portion + "%"
	else:
		return percent_str[:2] + "%"
