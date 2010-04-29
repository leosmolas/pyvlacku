from xml.sax import ContentHandler

class Parser(ContentHandler):
	def __init__(self):
		self.list = []
		
    def startElement(self, name, attrs):        
		if name == 'valsi':
			word = attrs.get('word')
			type = attrs.get('type')
			self.list+={'word':word,'type':type}
		
