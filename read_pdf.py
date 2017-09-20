#! usr/bin/python3

import PyPDF2

'''
This file is meant to open and extract text from a PDF file for the Russell 2000. 
The Russell 2000 file is downloaded from https://ftserussell.com
'''

pdfFileObj = open('ru2000_membershiplist_20170626.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

number_of_pages = int(pdfReader.numPages)
print(number_of_pages)

