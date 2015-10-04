#Python 2 project because Mechanize
#to-do: follow_link or click_link instead of open
import requests
import bs4
import mechanize
import cookielib
import json
import time

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

class stock:
	base_page = "https://www.predictit.org/Contract/"
	base_data = 'https://www.predictit.org/Home/GetChartPriceData?contractId='
	def __init__(self, link=None, contract_id=None):
		if contract_id:
			self.contract_id = str(contract_id)
			self.link = "{}{}".format(stock.base_page, contract_id)
		elif link:
			self.link = link
			link_parts = [x.lower() for x in link.split('/')]
			self.contract_id = link_parts[link_parts.index('contract')+1]
			#print(self.contract_id)
		else:
			raise TypeError
		url_data = "{}{}&timespan={}".format(stock.base_data, self.contract_id, "90D")
		#print(url_data)
		html_data = requests.get(url_data, verify=False).text
		self.data = json.loads(html_data)
		#self.url = link
		#page = br.open(link)
		#html = page.read()
		#soup = bs4.BeautifulSoup(html)
		#self.parse(soup)
	def parse(self, soup):
		pass
	def save(self, save_dir = "data"):
		#make the directory "/data"
		with open("{}/{}.json".format(save_dir, self.contract_id), 'w') as f:
			json.dump(self.data, f)

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
		repubs[candidate['name']] = (stock(link=candidate['link']))
		time.sleep(0.5)
	csv = "name," + ",".join([str(x) for x in list(range(90))]) + "\n"
	for name, data in repubs.items():
		row = [name]+[datapoint["PricePerShare"] for datapoint in data.data]
		csv+= ",".join([str(x) for x in row]) + "\n"
	with open("data/r/repubs.csv", 'w') as f:
		f.write(csv)
	return repubs

		

def save_all(start_at = 432, end_at = 1500):
	import time
	import random
	for i in range(start_at, end_at):
		x = stock(contract_id = i)
		x.save()
		time.sleep(random.random() + 0.7)

b = stock(contract_id = "523")
#rs = get_repubs()
#for r in rs:
#	r.save('data/r')

def leggo():
	p = br.open("https://www.predictit.org/")
	with open("yolo.txt", 'w') as f:
		f.write(p.read())
	x = br.follow_link(br.find_link(url='#SignInModal'))
	with open("yolomodal", "w") as f:
		f.write(x.read())
	print(x.read())
	print(x.read() == p.read())
	for form in br.forms():
		if form.attrs.get('id') == 'loginForm':
			br.form = form
	print(br.form)
	for control in br.form.controls:
		print(control)
leggo()