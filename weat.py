from flask import Flask, render_template
from bs4 import BeautifulSoup
import urllib2

app = Flask(__name__)

url = "https://weather.com/weather/today/l/THXX0055:1:TH"
url10 = "https://weather.com/weather/tenday/l/THXX0055:1:TH"

def cel(f):
	try :
		pr = str(int(round(((int(f.replace(u'\N{DEGREE SIGN}', ''))-32)*5)/9.0))) + u'\N{DEGREE SIGN}' +'C'
	except :
		pr = f
	return pr

def kmph(mph):
	try :
		#s = [str(a) for a in mph.split(' ')]
		i = [int(a) for a in mph.split(' ') if a.isdigit()]
		pr = str(int(round(i[0]*1.609344))) + ' kmph' # s[0] is the direction
	except : 
		pr = mph
	return pr

class get :
	def __init__ (self, time, temp, phrase, feel, hl, wind, hum, prec, id):
		self.time = time
		self.temp = temp
		self.phrase = phrase
		self.feel = feel
		self.hl = hl
		self.wind = wind
		self.hum = hum
		self.prec = prec
		self.id = id

@app.route('/')
def index():
	soup = BeautifulSoup(urllib2.urlopen(url))
	n = ''
	location = soup.select_one('h1.h4.today_nowcard-location').text

	time = soup.select_one('p.today_nowcard-timestamp').text.replace("ICT","")
	temp = cel(soup.select_one('div.today_nowcard-temp').text)
	phrase = soup.select_one('div.today_nowcard-phrase').text
	feel = cel(soup.select_one('span.deg-feels').text)
	hl = [cel(s.text) for s in soup.select('span.deg-hilo-nowcard > span')]
	side = soup.select('div.today_nowcard-sidecar > table > tbody > tr > td > span')
	now=get(time, temp, phrase, feel, hl, kmph(side[0].text), side[1].text, n, 0)

	soup = BeautifulSoup(urllib2.urlopen(url10)).select('tr.clickable')
	time = [soup[i].select_one('span.date-time').text + ' ' + soup[i].select_one('span.day-detail').text for i in range(0,3)]
	desc = [soup[i].select_one('td.description').text for i in range(0,3)]
	hl = [[cel(s.text) for s in soup[i].select('td.temp > div > span.')] for i in range(0,3)]
	prec = [soup[i].select_one('td.precip > div > span.').text for i in range(0,3)]
	wind = [kmph(soup[i].select_one('td.wind > span.').text) for i in range(0,3)]
	hum = [soup[i].select_one('td.humidity > span.').text for i in range(0,3)]
	days = [get(time[i], n, desc[i], n, hl[i], wind[i], hum[i], prec[i], i+1) for i in range(0,3) ]

	return render_template('weather.html', location=location, now=now, days=days)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=7000, debug=True)