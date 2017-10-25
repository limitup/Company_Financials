#!/usr/bin/env python3

from PyPDF2 import PdfFileReader
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import os
import re

# browser = webdriver.Chrome()
# browser.quit()


pdfFileObj = open('ru2000_membershiplist_20170626.pdf', 'rb')
pdfReader = PdfFileReader(pdfFileObj)

def get_symbols():
	'''
	This file is meant to open and extract text from a PDF file for the Russell 2000. 
	The Russell 2000 file is downloaded from https://ftserussell.com
	'''
	number_of_pages = pdfReader.getNumPages()

	text = ""
	for page in range(0,number_of_pages-1):
		pageObj = pdfReader.getPage(page)
		text += pageObj.extractText()

	symbol_list = []
	text = text.split('\n')
	for i in text:
		symbol = i.rstrip()
		if re.search('^[A-Za-z]{2,4}$',symbol):
			symbol_list.append(symbol)

	return symbol_list

if __name__ == '__main__':
	symbols = get_symbols()
	print(symbols)
	print(len(symbols))
