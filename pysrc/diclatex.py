# -*- coding: utf-8 -*-
import string
import codecs
import re

type2short = {'gismu':'g','fu\'ivla':'f','lujvo':'l','cmene':'n','cmavo':'c','cmavo cluster':'cc','experimental gismu':'eg'}

def letter2jbo(letter):
	letter.lower()
	if letter in ('a','e','i','o','u'):
		return '.' + letter + 'bu'
	elif letter=='y':
		return "y'y"
	else:
		return letter + 'y.'
		
def braces2links(s):
	def f(s):
		return "\\hyperlink{val:%s}{%s}" % (s.group(1).replace("'","h"), s.group(1)) #I don't really understand this line...
	return re.sub(r'\{(.+?)\}', f, s) #r"\\hyperref[val:\1]{\2}"

		
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
			f.write(u'\\phantomsection\\addcontentsline{toc}{section}{%s}\n \\dictchar{%s}\n' % (unicode(newLetter),unicode(newLetter)))
		f.write(u'\\hypertarget{val:%s}{\\0}' % (unicode(word).replace("'","h")))
		f.write(u'\\dictentry{%s}{}{%s}{' % (unicode(word),unicode(type2short[type])))
		if 'rafsi' in valsi:
			f.write('\\textit{%s}\\\\' % unicode(valsi['rafsi']))
		if 'selmaho' in valsi:
			f.write('\\textbf{%s}' % valsi['selmaho'])
		f.write(u'}\n {}{}{}{%s'% valsi['definition'])
		if 'notes' in valsi:
			f.write(u'\\\\ \\textit{%s}' % braces2links(valsi['notes']))
		f.write(u'}\n\n')
	f.close()

