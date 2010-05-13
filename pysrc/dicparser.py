# -*- coding: utf-8 -*-
    # pyvlacku
	# Lojban dictionary
    # Copyright (C) 2010  Leo Molas

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.
	
	#My e-mail: leos(dot)molas(at)gmail(dot)com
from xml.sax import ContentHandler
import string
import re

escape= {u'&':u'\\&',
		 u'%':u'\\%',
		 u'#':u'\\#',
		 # '{':'\\{',
		 # '}':'\\{',
		 u'\n':u'',
		 # '\\':'/'
		 u'€':u'\euro', #this command is provided by the package eurosym
		 u'’':u"'"
		 }

def substitute(s):
	keys = escape.keys()
	for i in range(len(keys)):
		# s = re.sub(r'\\', r'\\backslash ',s)
		s = s.replace(keys[i],escape[keys[i]])
	return s

class DicParser(ContentHandler):
	def __init__(self):
		#list with dictionaries (or associative arrays), which have all the entries, like valsi, selma'o, definition and notes
		self.list = []
		self.inverseList = []
		self.inverse = False #if true, we are on lojban to X. if false, X  to lojban
		#this variables
		self.inSelmaho = False
		self.inDefinition = False
		self.inNotes = False
		self.inRafsi = False
		(self.selmaho,self.valsi,self.notes,self.rafsi) = ('','','','')
		
	def startElement(self, name, attrs):
		if name == 'direction':
			self.inverse = attrs.get('to') == 'lojban'
		elif self.inverse:
			self.parseInverse(name,attrs)
		else:
			self.parseDirect(name,attrs)
			
	def parseDirect(self,name,attrs):
		if name == 'valsi':
			self.word = attrs.get('word')
			self.type = attrs.get('type')
			self.list+=[{u'word':self.word,u'type':self.type}]
		elif name == 'selmaho':
			self.inSelmaho = True
			self.selmaho = ""
		elif name == 'definition':
			self.inDefinition = True
			self.definition = ""
		elif name == 'notes':
			self.inNotes = True
			self.notes = ""
		elif name == 'rafsi':
			self.inRafsi = True
			self.rafsi = ""
		
	def parseInverse(self,name,attrs):
		if name == "nlword":
			dict = {}
			dict['word'] = substitute(attrs.get('word'))
			dict['valsi'] = attrs.get('valsi')
			if 'sense' in attrs:
				dict['sense'] = substitute(attrs.get('sense'))
			if 'place' in attrs:
				dict['place'] = int(attrs.get('place'))
			self.inverseList += [dict]
	
	def characters(self,ch):
		ch = substitute(ch)
		if self.inSelmaho:
			self.selmaho += ch
		elif self.inDefinition:
			self.definition += ch
		elif self.inNotes:
			self.notes += ch
		elif self.inRafsi:
			self.rafsi += ch
			
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
		elif name == 'rafsi':
			self.list[-1][name] = self.rafsi
			self.inRafsi = False
		