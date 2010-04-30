# -*- coding: utf-8 -*-
import string
import codecs

type2short = {'gismu':'g','fu\'ivla':'f','lujvo':'l','cmene':'n','cmavo':'c','cmavo cluster':'cc','experimental gismu':'eg'}

def letter2jbo(letter):
	letter.lower()
	if letter in ('a','e','i','o','u'):
		return '.' + letter + 'bu'
	elif letter=='y':
		return "y'y"
	else:
		return letter + 'y.'
		
def list2tex (list,file):
	f = codecs.open(file, "w", "mbcs")#utf_8_sig
		
	result = ""
	currentLetter = ' '
	for i in range(len(list)):
		valsi = list[i]
		word = valsi['word']
		type = valsi['type']
		if word[0]!=currentLetter:
			currentLetter = word[0]
			newLetter = letter2jbo(currentLetter)
			f.write(u'\\addcontentsline{toc}{subsection}{' + unicode(newLetter) +u'}\n' +
					u'\\dictchar{'+ unicode(newLetter)+u'}\n')
		#f.write(u'\\hypertarget{val:' + unicode(word) + u'}{}\n')
		f.write(u'\\dictentry{' + unicode(word) + u'}{}{' + unicode(type2short[type]) + u'}{')
		if 'rafsi' in valsi:
			f.write(unicode(valsi['rafsi']) + u'\\\\')
		if 'selmaho' in valsi:
			f.write(unicode(valsi['selmaho']))
		f.write(u'}\n' +
				u'{}{}{}{' + unicode(valsi['definition']))
		if 'notes' in valsi:
			f.write(u'\\\\ \\textit{' + unicode(valsi['notes']) + u'}')
		f.write(u'}\n')
	f.close()

