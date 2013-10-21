import datetime

def parse_date(date_str):
	"""
	Parses the date passed in through the argument date_str
	Parses in the format MM/DD/YYYY
	"""
	date_str = date_str.replace("-", "/")
	
	date_fields = date_str.split("/")
	month = date_fields[0]
	day = date_fields[1]
	year = date_fields[2]
	
	if(len(year) == 2):	#changes the year from a 2 digit to a 4 digit date
		year = "20" + year

	#Validate
	try:
		day_int = int(day)
		month_int = int(month)
		year_int = int(year)
		
		print(str(day_int) + " " + str(month_int) + " " + str(year_int))
		
		date = datetime.datetime(year_int, month_int, day_int)
	except ValueError:
		print("VALUE ERROR")
		date = None
		
	return date

def parse_date_iso(iso_date_str):
	"""
	Parse the date passed in through the argument iso_date_str
	Parses in the ISO format YYYY-MM-DD
	Does not do as many validation checks, because this method should not be used to parse user inputed data
	"""
	date_fields = iso_date_str.split("-")
	print(str(date_fields))
	month = date_fields[0]
	day = date_fields[1]
	year = date_fields[2]
	
	datetime.datetime(year_int, month_int, day_int)

def parse_date_to_string(date):
	"""
	Gets a dae object then returns a string representation
	In format MM/DD/YYYY
	"""
	return str(date.month) + "/" + str(date.day) + "/" + str(date.year)
