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

if __name__ == '__main__':
	# Create a parser
	p = make_parser()

    # Tell the parser we are not interested in XML namespaces
	p.setFeature(feature_namespaces, 0)

    # Create the handler
	dh = DicParser()

    # Tell the parser to use our handler
	p.setContentHandler(dh)

    # Parse the input
	p.parse('spanish.xml')
	
	f = codecs.open('jbocas.tex', "w", sys.getfilesystemencoding()) #this magic function make the script to be OS independant
	# Create the .tex file from the list obtained, writing the section 
	diclatex.list2TeX(dh.list, f)
	f.close()
	g =  codecs.open('casjbo.tex', "w", sys.getfilesystemencoding())
	diclatex.inverseList2TeX(dh.inverseList,g)
	g.close()
