TWO_LETTER_ABBREV = {
	"Ex":"Exodus",
	"Ez":"Ezra"
}

BIBLE_CHAPTERS = {
	"Genesis":50,
	"Exodus":40,
	"Leviticus":27,
	"Numbers":36,
	"Deuteronomy":34,
	"Joshua":24,
	"Judges":21,
	"Ruth":4,
	"1 Samuel":31,
	"2 Samuel":24,
	"1 Kings":22,
	"2 Kings":25,
	"1 Chronicles":29,
	"2 Chronicles":36,
	"Ezra":10,
	"Nehemiah":13,
	"Esther":10,
	"Job":42,
	"Psalms":150,
	"Proverbs":31,
	"Ecclesiastes":12,
	"Song of Solomon":8,
	"Isaiah":66,
	"Jeremiah":52,
	"Lamentations":5,
	"Ezekiel":48,
	"Daniel":12,
	"Hosea":14,
	"Joel":3,
	"Amos":9,
	"Obadiah":1,
	"Jonah":4,
	"Micah":7,
	"Nahum":3,
	"Habakkuk":3,
	"Zephaniah":3,
	"Haggai":2,
	"Zechariah":14,
	"Malachi":4,
	
	"Matthew":28,
	"Mark":16,
	"Luke":24,
	"John":21,
	"Acts":28,
	"Romans":16,
	"1 Corinthians":16,
	"2 Corinthians":13,
	"Galatians":6,
	"Ephesians":6,
	"Philippians":4,
	"Colossians":4,
	"1 Thessalonians":5,
	"2 Thessalonians":3,
	"1 Timothy":6,
	"2 Timothy":4,
	"Titus":3,
	"Philemon":1,
	"Hebrews":13,
	"James":5,
	"1 Peter":5,
	"2 Peter":3,
	"1 John":5,
	"2 John":1,
	"3 John":1,
	"Jude":1,
	"Revelation":22
}

def parse_reading(reading_str):
	"""
	Parses the string to a bible chapter
	"""

	#make sure reading_str exists or is valid
	if(reading_str == None or len(reading_str) == 0):
		return None

	reading_str = reading_str.replace(" ", "")
	reading_str = reading_str.replace(":", "")
	reading_str = reading_str.replace(".", "")

	#get the index of the chapter
	chapter_index = 0
	for i in range(1, len(reading_str)):
		if(reading_str[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9') and chapter_index == 0):
			chapter_index = i
	
	book = reading_str[:chapter_index]
	chapter = reading_str[chapter_index:]
	
	#handles inputting multiple chapters on the same line
	chapters_str = chapter.split("-")
	chapters = []
	if(len(chapters_str) == 1):	#only one chapter
		if(chapter.isnumeric()):
			chapters = [chapter]
	elif(len(chapters_str) == 2):
		if(chapters_str[0].isnumeric() and chapters_str[1].isnumeric()):
			chapters = range(int(chapters_str[0]), int(chapters_str[1])+1)
		
	
	#get the correct book name
	book_name = ""
	for full_book_name in BIBLE_CHAPTERS:
		if(full_book_name.replace(" ", "").startswith(book)):
			book_name = full_book_name
	
	if(book_name == ""):	#not a valid book
		return None
	
	#return all the chapters in a list of strings with format BOOK CHAPTER
	chapters_read = []
	for i in chapters:
		if(int(i) in range(1, BIBLE_CHAPTERS[book_name]+1)):	#checks to make sure that the chapter exists
			chapters_read.append(book_name + " " + str(i))
	
	if(len(chapters_read) == 0):
		return None
	else:
		return chapters_read
	
