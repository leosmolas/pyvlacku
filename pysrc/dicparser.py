from xml.sax import ContentHandler

class DicParser(ContentHandler):
	def __init__(self):
		#list with dictionaries (or associative arrays), which have all the entries, like valsi, selma'o, definition and notes
		self.list = []
		self.inSelmaho = False
		self.inDefinition = False
		self.inNotes = False
		
	def startElement(self, name, attrs):        
		if name == 'valsi':
			word = attrs.get('word')
			type = attrs.get('type')
			self.list+=[{u'word':word,u'type':type}]
		elif name == 'selmaho':
			self.inSelmaho = True
			self.selmaho = ""
		elif name == 'definition':
			self.inDefinition = True
			self.definition = ""
		elif name == 'notes':
			self.inNotes = True
			self.notes = ""
	
	def characters(self,ch):
		if self.inSelmaho:
			self.selmaho += ch
		elif self.inDefinition:
			self.definition += ch
		elif self.inNotes:
			self.notes += ch
			
	def endElement(self,name):
		if name == 'selmaho':
			self.list[-1][name] = self.selmaho
			self.inSelmaho = False
		elif name == 'definition':
			self.list[-1][name] = self.definition
			self.inDefinition = False
		elif name == 'notes':
			self.list[-1][name] = self.notes
			self.inNotes = False
		