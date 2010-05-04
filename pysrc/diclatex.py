# -*- coding: utf-8 -*-
import string
import re
import unicodedata


type2short = {	'gismu':'g',
				'fu\'ivla':'f',
				'lujvo':'l',
				'cmene':'n',
				'cmavo':'c',
				'cmavo cluster':'cc',
				'experimental gismu':'eg'}

#this go from place structure to the SE selma'o
place2SE = {2:u'se ',
			3:u'te ',
			4:u've ',
			5:u'xe '}
			
# def place2SE(i):
	# if i == 2:
		# return 'se '
	# elif i == 3:
		# return 'te '
	# elif i == 4:
		# return 've '
	# elif i == 5:
		# return 'xe '
	# else:
		# return ''

def letter2jbo(letter):
	letter.lower()
	if letter in ('a','e','i','o','u'):
		return '.' + letter + 'bu'
	elif letter=='y':
		return "y'y"
	else:
		return letter + 'y.'

def stripAccents(s):
	aux = ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')) #I don't understand this line either... it's just working :)
	if aux[0].isalpha() or aux[0].isdigit():
		return aux
	else:
		return aux[1:]

def braces2links(s):
	def f(s):
		return "\\hyperlink{val:%s}{%s}" % (s.group(1).replace("'","h"), s.group(1)) #I don't really understand this line...
	return re.sub(r'\{(.+?)\}', f, s) #r"\\hyperref[val:\1]{\2}"
	
def breakSlashes(s):
	return re.sub('/',r'\\fshyp{}\\discretionary{}{}{}',s)

def list2TeX (list,f):
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
		f.write(u'\\hypertarget{val:%s}{\\null}' % (unicode(word).replace("'","h"))) #this \null is there because it magically fixes a bug. When I left the second parameter of hypertarget empty, all the multicolumns enviroment breaks
		f.write(u'\\dictentry{%s}{}{%s}{' % (unicode(word),unicode(type2short[type])))
		if 'rafsi' in valsi:
			f.write('\\textit{%s}\\\\' % unicode(valsi['rafsi']))
		if 'selmaho' in valsi:
			f.write('\\textbf{%s}' % valsi['selmaho'])
		f.write(u'}\n {}{}{}{%s'% breakSlashes(valsi['definition']))
		if 'notes' in valsi:
			f.write(u'\\\\ \\textit{%s}' % braces2links(valsi['notes']))
		f.write(u'}\n\n')

def inverseList2TeX(list,f):
	list = sorted(list, key = lambda list:stripAccents(list['word']).lower()) #this weird line does magic to order the list
	# for i in range(len(list)):
		# print list[i]['word']
	result = u''
	currentLetter = u' '
	digit = False
	symbol = False
	for i in range(len(list)):
		entry = list[i]
		natWord = entry['word']
		if stripAccents(natWord)[0].upper()!=currentLetter:
			currentLetter = stripAccents(natWord[0]).upper()
			if not currentLetter.isdigit() and not currentLetter.isalpha():
				if not symbol:
					f.write(u'\\phantomsection \\addcontentsline{toc}{section}{\\#}\n\\dictchar{\\#}\n')
					symbol = True
			elif currentLetter.isdigit():
				if not digit:
					f.write(u'\\phantomsection \\addcontentsline{toc}{section}{123}\n \\dictchar{123}\n')
					digit = True
			else:
				f.write(u'\\phantomsection \\addcontentsline{toc}{section}{%s}\n \\dictchar{%s}\n' % (unicode(currentLetter),unicode(currentLetter)))
		f.write(u'\\dictentry{%s}{}{}{' % unicode(natWord))
		if 'sense' in entry:
			f.write(entry['sense'])
		if 'place' in entry:
			gloss = place2SE.get(entry['place'],u'') + entry['valsi']
		else:
			gloss = entry['valsi']
		f.write('}\n{\\hyperlink{val:%s}{%s}}{}{}{}\n\n'% (unicode(entry['valsi'].replace("'","h")),unicode(gloss)))
		