from datetime import date
import requests
import json
import pandas as pd
from read_pdf import get_symbols
import unittest

# EDGAR url format
# {Protocol}://edgaronline.api.mashery.com/{Version}/{Endpoints}{Format}?{Parameters}appkey={API Key}

"""
	Documentation can be found at http://developer.edgar-online.com/docs/core_financials
	-need company class for company description
	-need financials for balance sheet, income statement, cash flow
	-return financials in dataframe
"""

API_Key = 'Secret Key'

# Company MetaData
# http://edgaronline.api.mashery.com/v2/companies.json?primarysymbols=MSFT&appkey={API_Key}

# Company Core Financials
# http://edgaronline.api.mashery.com/v2/corefinancials/ann.json?primarysymbols=aapl&numperiods=1&appkey={API_Key}

class Company(object):
	"""
	docstring for Company class
	"""
	def __init__(self, symbol, API_Key):
		self.symbol = symbol
		self.API_Key = API_Key

		self.description = {}

	def company_metadata(self):
		base_url = 'http://edgaronline.api.mashery.com/v2/companies.json?'

		website = base_url+'primarysymbols='+self.symbol+'&appkey='+ self.API_Key
		r = requests.get(website)
		data = json.loads(r.text)
		company_data = data['result']['rows'][0]['values']

		#return company metadata values
		for i in company_data:
			self.description[i['field']] =  i['value']

	def __str__(self):
		return self.symbol

	def __dict__(self):
		return self.description


class CashFlow(Company):

	def __init__(self, symbol, API_Key):
		Company.__init__(self, symbol, API_Key)

	def annual_financials(self): 
		"""
		Return annual financials
		"""
		base_url = 'http://edgaronline.api.mashery.com/v2/'
		corefinancials = {'annual':'corefinancials/ann', 'quarter':'corefinancials/qtr'}
		numperiods = str(1) #default is 4 with Annual 

		website =  base_url+corefinancials['annual']+'?primarysymbols='+self.symbol+'&appkey='+API_Key
		r = requests.get(website)
		data = json.loads(r.text)
		company_data = data['result']['rows']
		for i in company_data:
			for j in i['values']:
				print(j['field'], j['value'])
			print()


	def quarterly_financials(self, symbol):
		"""
		Return company quarter financials
		"""
		pass

class IncomeStatement(Company):
	"""docstring for IncomeStatement"""
	def __init__(self):
		Company.__init__(self, symbol, API_Key)

	def annual(self):
		pass

	def quarterly(self):
		pass


class BalanceSheet(Company):
	def __init__(self):
		Company.__init__(self, symbol, API_Key)

	def annual(self):
		pass

	def quarterly(self):
		pass
		
if __name__ == '__main__':
	sample_company = Company('AAPL', API_Key)
	sample_company.company_metadata()
	print(sample_company.description)
	
	sample_financials = CashFlow('FB', API_Key)
	print(sample_financials.symbol)
	sample_financials.annual_financials()
