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
		
#This was copied and modified from the proyect vlasisku
# copyright: Copyright © 2010 Dag Odenhall <dag.odenhall@gmail.com>
# url: https://launchpad.net/vlasisku
# license: http://www.gnu.org/licenses/agpl-3.0.html
#def braces2links(text, entries):
def braces2links(text):
	"""Turns {quoted words} into HTML links.

	>>> import db
	>>> braces2links('See also {mupli}.', db.entries)
	'See also <a href="mupli" title="x<sub>1</sub> is
	an example/sample/specimen/instance/case/illustration of
	common property(s) x<sub>2</sub> of set x<sub>3</sub>.">mupli</a>.'
	>>> braces2links('See also {missing}.', db.entries)
	'See also <a
	href="http://jbovlaste.lojban.org/dict/addvalsi.html?valsi=missing"
	title="This word is missing, please add it!" class="missing">missing</a>.'
	"""
	
	"""I keeped those comments for historical reasons ... (?)
	My version converts {valsi} links into \ref{valsi}
	"""
	def f(m):
			# values = (m.group(1), entries[m.group(1)].definition, m.group(1))
			# return '<a href="%s" title="%s">%s</a>' % values
			return "\\ref{val:%s}" % (m)
		# except KeyError:
			# link = ['<a href="']
			# link.append('http://jbovlaste.lojban.org')
			# link.append('/dict/addvalsi.html?valsi=%s"')
			# link.append(' title="This word is missing, please add it!"')
			# link.append(' class="missing">%s</a>')
			# return ''.join(link) % (m.group(1), m.group(1))
	return re.sub('\{(.+?)\}', f, text)
	
"""well... my needed something muuuuuuuuch more simple. The difference is that, if the word is not found, LaTeX handles it, putting a ?? I think. This may be changed in the future.
Thanks donri for the great work with vlasisku :)"""
		
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
		#f.write(u'\\hypertarget{val:' + unicode(word) + u'}{}\n')
		f.write(u'\\phantomsection\\dictentry{' + unicode(word) + u'}{}{' + unicode(type2short[type]) + u'}{')
		if 'rafsi' in valsi:
			f.write(unicode(valsi['rafsi']) + u'\\\\')
		if 'selmaho' in valsi:
			f.write(unicode(valsi['selmaho']))
		f.write(u'}\n' +
				u'{}{}{}{' + unicode(valsi['definition']))
		if 'notes' in valsi:
			f.write(u'\\\\ \\textit{' + braces2links(valsi['notes']) + u'}')
		f.write(u'}\n')
	f.close()

