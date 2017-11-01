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

		df = pd.DataFrame.from_dict(self.description, orient='index')
		return df

	def __str__(self):
		return self.symbol


class Financials(Company):

	def __init__(self, symbol, API_Key):
		Company.__init__(self, symbol, API_Key)

	def financials(self, statement= None, period= None): 
		"""
		Return annual financials
		"""
		base_url = 'http://edgaronline.api.mashery.com/v2/'
		corefinancials = {'Annual':'corefinancials/ann', 'Quarter':'corefinancials/qtr'}
		financialstatement = {'CashFlow':'CashFlowStatementConsolidated', 'BalanceSheet':'BalanceSheetConsolidated', 'IncomeStatement':'IncomeStatementConsolidated'}

		website =  base_url+corefinancials[period]+'?primarysymbols='+self.symbol+'&fields='+financialstatement[statement]+'&appkey='+API_Key
		r = requests.get(website)
		data = json.loads(r.text)

		# Need to combine each year to individual df and concat to other years
		df_each_year = []
		company_data = data['result']['rows']
		for i in company_data:
			cashflow = {}
			for j in i['values']:
				# print(j['field'], j['value'])
				cashflow[j['field']] = j['value']
			# returns df without fiscal year as column headers
			df = pd.DataFrame.from_dict(cashflow, orient= 'index')
			df_each_year.append(df)

		return pd.concat(df_each_year[::-1], axis=1)

		
if __name__ == '__main__':
	sample_financials = Financials('AAPL', API_Key)
	# print(sample_financials.symbol)
	sample_financials.company_metadata()
	statement = sample_financials.financials(period='Annual', statement ='IncomeStatement')
	print(statement)
