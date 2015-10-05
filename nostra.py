#Python 2 project because Mechanize
#to-do: follow_link or click_link instead of open
import requests
import bs4
import mechanize
import cookielib
import json
import time
import config
import urllib
from math import copysign

#import requests.packages.urllib3 #lol
#requests.packages.urllib3.disable_warnings() #lol hackathon
import os
if not os.path.exists("data"):
	os.makedirs("data")


#following br setup code from http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/
# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'),
                 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                 ('Accept-Language', 'en-US,en;q=0.5'),
                 ('Accept-Encoding', 'gzip, deflate'),
                 ('Connection', 'keep-alive')]


#index_page = br.open("https://www.predictit.org/Browse/Featured")
#html = index_page.read()

#soup = bs4.BeautifulSoup(html)
#print(soup.find("Greece"))

def login():
	pass

#contract_id = 1277
#here = 'https://www.predictit.org/Home/GetChartPriceData?contractId='
#contract = "{base}{contract_id}&timespan={days}".format(base=here, contract_id=contract_id, days="90D")
#print(contract)
#print(requests.get(contract).text)
class Sentiment:
	def __init__(self, *args):
		#self.biden_positivity = requests.get("url goes here").text
		self.positivity = 0.5
	def hardcode_sentiment(self, hc):
		self.positivity = hc

class Trader:
	def __init__(self, email, password):
		self.login(email, password)
	def login(self, email, password):
		p = br.open("https://www.predictit.org/")
		#with open("yolo.txt", 'w') as f:
		#	f.write(p.read())
		x = br.follow_link(br.find_link(url='#SignInModal'))
		#with open("yolomodal", "w") as f:
		#	f.write(x.read())
		#print(x.read())
		#print(x.read() == p.read())
		for form in br.forms():
			if form.attrs.get('id') == 'loginForm':
				br.form = form
		#print(br.form)
		#for control in br.form.controls:
	#		print(control)
		br.form["Email"] = config.email
		br.form["Password"] = config.password
		response = br.submit()
	#print(response.read())

class Stock:
	base_page = "https://www.predictit.org/Contract/"
	base_data = 'https://www.predictit.org/Home/GetChartPriceData?contractId='
	def __init__(self, link=None, contract_id=None):
		if contract_id:
			self.contract_id = str(contract_id)
			self.link = "{}{}".format(Stock.base_page, contract_id)
		elif link:
			self.link = link
			link_parts = [x.lower() for x in link.split('/')]
			self.contract_id = link_parts[link_parts.index('contract')+1]
			#print(self.contract_id)
		else:
			raise TypeError
		url_data = "{}{}&timespan={}".format(Stock.base_data, self.contract_id, "90D")
		#print(url_data)
		html_data = requests.get(url_data, verify=False).text
		self.data = json.loads(html_data)
		#self.url = link
		########the stuff below was commented out earlier and I don't remember why so fuck hackathons
		page = br.open(self.link)
		html = page.read()
		soup = bs4.BeautifulSoup(html)
		self.parse(soup)
		#########end stuff
	#def refresh_page(self):
	def refresh_and_parse(self):
		page = br.open(self.link)
		html = page.read()
		soup = bs4.BeautifulSoup(html)
		self.parse(soup)
	def parse(self, soup):
		soup.find("div")
	def save(self, save_dir = "data"):
		#make the directory "/data"
		with open("{}/{}.json".format(save_dir, self.contract_id), 'w') as f:
			json.dump(self.data, f)
	def trade_on_sentiment(self, contract_id, bluemix_sentiment):
		current_price = 0.61
		bluemix_sentiment = bluemix_sentiment.positivity
		difference = bluemix_sentiment - current_price
		amount_to_buy = abs(int(difference * 25))
		yes = int(difference > 0)
		#bluemix_sentiment
		print("Bluemix sentiment is {}.  Current yes price is {}".format(bluemix_sentiment, current_price, int(bluemix_sentiment*5)))
		print("Sentiment - Price = {}.  Buying {} {} stocks.".format(difference, abs(int(difference * 25)), ('NO', 'YES')[yes]))
		buy_stock(contract_id, amount_to_buy, yes, current_price)


def get_repubs():
	if not os.path.exists("data/r"):
		os.makedirs("data/r")
	repubs = dict()
	#index_page = br.open("https://www.predictit.org/Market/1233/Who-will-win-the-2016-Republican-presidential-nomination")
	index_page = br.open("https://www.predictit.org/Home/GetContractListAjax?marketId=1233")
	soup = bs4.BeautifulSoup(index_page.read())
	candidates = soup.findAll('tr')
	h = 0
	for i in candidates[1:]:
		candidate = dict()
		try:
			candidate['name'] = i.find("h4").text
		except AttributeError: #rewrite this if there can be a table row that we want that comes after a table row without an h4
			break
		candidate['link'] = "https://www.predictit.org" + i.find('a')['href']
		for price, key in zip(i.findAll('td')[-4:], ['BuyY', 'SellY', 'BuyN', 'SellN']):
			candidate[key] = price.text.strip().rstrip(u'\xa2') #strip the cent sign.
		print(candidate)
		#repubs.append(candidate)
		repubs[candidate['name']] = (Stock(link=candidate['link']))
		time.sleep(0.5)
	csv = "name," + ",".join([str(x) for x in list(range(90))]) + "\n"
	for name, data in repubs.items():
		row = [name]+[datapoint["PricePerShare"] for datapoint in data.data]
		csv+= ",".join([str(x) for x in row]) + "\n"
	with open("data/r/repubs.csv", 'w') as f:
		f.write(csv)
	return repubs

		

def save_all(start_at = 432, end_at = 1500, save_dir="data"):
	import time
	import random
	for i in range(start_at, end_at):
		x = Stock(contract_id = i)
		x.save(save_dir)
		time.sleep(random.random() + 0.7)

b = Stock(contract_id = "523")
#rs = get_repubs()
#for r in rs:
#	r.save('data/r')

def login():
	p = br.open("https://www.predictit.org/")
	#with open("yolo.txt", 'w') as f:
	#	f.write(p.read())
	x = br.follow_link(br.find_link(url='#SignInModal'))
	#with open("yolomodal", "w") as f:
	#	f.write(x.read())
	#print(x.read())
	#print(x.read() == p.read())
	for form in br.forms():
		if form.attrs.get('id') == 'loginForm':
			br.form = form
	#print(br.form)
	#for control in br.form.controls:
#		print(control)
	br.form["Email"] = config.email
	br.form["Password"] = config.password
	response = br.submit()
	#print(response.read())


login()

def buy_stock(contract_id, quantity, yes, price):
	"""yes is 1 if the stock is "yes stock" and is 0 if the stock is "no stock" """
	if type(yes) == bool:
		yes = int(yes)
	#print(cj)
	request = mechanize.Request("https://www.predictit.org/Contract/{}".format(contract_id))
	response = br.open(request)#, data=dat)
	
	k = br.open("https://www.predictit.org/Trade/LoadShort?contractId={}".format(contract_id))
	s = bs4.BeautifulSoup(k.read())
	vtoken = s.find('input', attrs = {'name':'__RequestVerificationToken'}).get('value')
	
	params = {u'__RequestVerificationToken': vtoken, u'TradeType': yes, u'Quantity': quantity, u'ContractId': contract_id, u'PricePerShare': price, u'X-Requested-With': 'XMLHttpRequest'}
	dat = urllib.urlencode(params)
	request = mechanize.Request("https://www.predictit.org/Trade/ConfirmTrade")
	response = br.open(request, data = dat)

	vtoken = s.find('input', attrs = {'name':'__RequestVerificationToken'}).get('value')
	params = {u'__RequestVerificationToken': vtoken, u'BuySellViewModel.TradeType': yes, u'BuySellViewModel.Quantity': quantity, u'BuySellViewModel.ContractId': contract_id, u'BuySellViewModel.PricePerShare': price, u'X-Requested-With': 'XMLHttpRequest'}
	dat = urllib.urlencode(params)
	request = mechanize.Request("https://www.predictit.org/Trade/SubmitTrade")
	response = br.open(request, data = dat)
	print("bought {} {} stock of {} for ${} each.".format(quantity, ('NO', 'YES')[yes], contract_id, price))

def all_in(contract_id, yes):
	import urllib
	request = mechanize.Request("https://www.predictit.org/Contract/{}".format(contract_id))
	response = br.open(request)#, data=dat)
	
	soup = bs4.BeautifulSoup(response.read())
	prices = soup.find('div', _class="panel-body offers")
	print(prices.text)



def trade_on_sentiment(contract_id, bluemix_sentiment):
	current_price = 0.61
	bluemix_sentiment = bluemix_sentiment.positivity
	difference = bluemix_sentiment - current_price
	amount_to_buy = abs(int(difference * 25))
	yes = int(difference > 0)
	#bluemix_sentiment
	print("Bluemix sentiment is {}.  Current yes price is {}".format(bluemix_sentiment, current_price, int(bluemix_sentiment*5)))
	print("Sentiment - Price = {}.  Buying {} {} stocks.".format(difference, abs(int(difference * 25)), ('NO', 'YES')[yes]))
	buy_stock(contract_id, amount_to_buy, yes, current_price)


#all_in('1277', 0)
biden_positivity = Sentiment('Biden, running')
trade_on_sentiment(1277, bluemix_sentiment=biden_positivity)

#s = buy_stock('1277', 1, 0, 0.57)