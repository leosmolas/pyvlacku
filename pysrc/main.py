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

from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from dicparser import DicParser
import diclatex
import codecs
import sys

"""The program should be called with three parameters: 
First, the xml
Then, the direct dictionary
Finally, the inverse dictionary
The default values are 'english.xml', 'lojen.tex' and 'enloj.tex', respectively.
If it's called with only one argument, it is taken as the xml file
If it's called with two, the program ignores the second one.
If it's calle with more than three, the program ignores the latests
If any of the parameters is '--help', the program print this"""

if __name__ == '__main__':
#count returns the number of aparitions of the parameter
	if sys.argv.count('--help')>0:
		print """The program should be called with three parameters: 
First, the xml
Then, the direct dictionary
Finally, the inverse dictionary
The default values are 'english.xml', 'lojen.tex' and 'enloj.tex', respectively.
If it's called with only one argument, it is taken as the xml file
If it's called with two, the program ignores the second one.
If it's calle with more than three, the program ignores the latests
If any of the parameters is '--help', the program print this"""
	elif len(sys.argv)>3:
		xml     = sys.argv[1]
		direct  = sys.argv[2]
		inverse = sys.argv[3]
	elif len(sys.argv)>1:
		xml     = sys.argv[1]
		direct  = 'lojen.tex'
		inverse = 'enloj.tex'
	else:
		xml     = 'english.xml'
		direct  = 'lojen.tex'
		inverse = 'enloj.tex'
	# Create a parser
	p = make_parser()

    # Tell the parser we are not interested in XML namespaces
	p.setFeature(feature_namespaces, 0)

    # Create the handler
	dh = DicParser()

    # Tell the parser to use our handler
	p.setContentHandler(dh)

    # Parse the input
	p.parse(xml)
	
	f = codecs.open(direct, "w", sys.getfilesystemencoding()) #this magic function make the script to be OS independant 
	#you might change it with 'mbcs' (ansi) or 'utf-8'
	# Create the .tex file from the list obtained, writing the section 
	diclatex.list2TeX(dh.list, f)
	f.close()
	g =  codecs.open(inverse, "w", sys.getfilesystemencoding())
	diclatex.inverseList2TeX(dh.inverseList,g)
	g.close()
