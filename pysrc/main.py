# -*- coding: utf-8 -*-
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from dicparser import DicParser
import diclatex

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
	
	# Create the .tex file from the list obtained
	diclatex.list2tex(dh.list, 'jbocas.tex')
