
import requests, bs4

# create my data structure [ {'home': 'home_team',
#								'away': 'away_team',
#								'home_win: list['home_win_odds'],
#								'draw': list['draw_odds'],
#								'away_win': list['away_win_odds']},
#								...]
# a list of dictionaries, where each dictionary contains the predictions for that game
# the value stored by the '_win' key is a list of floats representing the 
# odds from some site 

# initialize data structure

def initData():
	data = []
	for i in range(0,10):
		dict = {}
		dict['home'] = ""
		dict['away'] = ""
		dict['home_win'] = []
		dict['draw'] = []
		dict['away_win'] = []
		data.append(dict)
	return data	

def getSkyBetData(data):		
	site = 'https://www.skybet.com/football/premier-league'
	res = requests.get(site)
	soupObject = bs4.BeautifulSoup(res.text, 'lxml')

	game_days = soupObject.select('div[class="market-wdw"]') # list 

	print("SkyBet Data")
	print("Home Win		Draw		Away Win")
	
	game_number = 0
	for day in game_days:
		table = day.select("table")
		tbody = table[0].select("tbody")
		tr_list = tbody[0].select("tr") # this a list representing rows of games that day
			
		print(len(tr_list))
		for tr in tr_list: # for each game in the game week
		
			# initialize the dictionary
			dictionary = data[game_number]
			
			td = tr.select("td") # left hand side is a list 
			a = td[1].select("a") # skip the first td in the list 
			home = a[0]['data-oc-desc']
			dictionary['home'] = home # name of the home team 
			
			# odds of the home team winning
			num = float(a[0]['data-oc-price-num']) 
			den = float(a[0]['data-oc-price-den'])
			odds = num/den
			dictionary['home_win'].append(odds)
			
			# format display
			odds_home_win = "{:.2f}".format(odds)
			left = "{:25}".format(home + ": " + odds_home_win) # display
			
			# get the odds of a draw
			a = td[2].select("a")
			num = float(a[0]['data-oc-price-num'])
			den = float(a[0]['data-oc-price-den'])
			odds = num/den 
			dictionary['draw'].append(odds)
			
			# format display 
			odds_draw = "{:.2f}".format(num/den)
			mid = "{:20}".format("Draw: " + odds_draw)
			
			# get the odds of the other team winning
			a = td[3].select("a")
			away = a[0]['data-oc-desc']
			dictionary['away'] = away
			num = float(a[0]['data-oc-price-num'])
			den = float(a[0]['data-oc-price-den'])
			odds = num/den
			dictionary['away_win'].append(odds)
			
			# format display
			odds_away_win = "{:.2f}".format(num/den)
			right = "{:20}".format(away + ": " + odds_away_win)
			
			# print formatted display
			print(left + mid + right)
			print("")
			
			game_number = game_number + 1
	return data
			
			
		
		
def getOddsCheckerData(data):
	
	site = 'http://www.oddschecker.com/football/english/premier-league'
	res = requests.get(site)
	soupObject = bs4.BeautifulSoup(res.text, 'lxml')
	# integer will be derived from theSkybet script, num of game_days that week
	gameDays = 2 
	tags = soupObject.select('div[id="fixtures"]')
	tags = tags[0].select('div[class="content-4"]')
	table = tags[0].select('table')
	tbody = table[0].select('tbody')
	tr = tbody[0].select('tr[data-mid]')

	game_number = 0 # enumerate each game of the week from 1 to 10
	for game in tr: # each game in a table row
		
		# this site displays games for the upcoming two weeks
		if (game_number == 10):
			break
			
		td = game.select('td[data-bid]')

		home = td[0]['title']
		home = home.split()[1]
		home_win_odds = td[0]['data-best-odds']
		home_win_odds = float(home_win_odds)

		draw_odds = td[1]['data-best-odds']
		draw_odds = float(draw_odds)
		
		away = td[2]['title']
		away = away.split()[1]
		away_win_odds = td[2]['data-best-odds']
		away_win_odds = float(away_win_odds)
		
		data[game_number]['home_win'].append(home_win_odds)
		data[game_number]['draw'].append(draw_odds)
		data[game_number]['away_win'].append(away_win_odds)
		
		print(game_number)
		print(home + str(home_win_odds))
		
		game_number = game_number + 1
		
	return data 	

def displayData(data):
	
	print("Average Odds")
	print("Home				 	Away")
	
	for game in data:
		
		odds_list = game['home_win'] # list containing odds from diff sites
		sum = 0.0
		counter = 0
		for odds in odds_list:
			sum = sum + odds
			counter = counter + 1
		average = sum/counter 		
		odds_home_win = "{:.2f}".format(average)
		left = "{:25}".format(game['home'] + ": " + odds_home_win) # display
			
		# format display
		odds_list = game['draw']
		sum = 0.0
		counter = 0
		for odds in odds_list:
			sum = sum + odds
			counter = counter + 1
		
		average = sum/counter 		
		draw_odds = "{:.2f}".format(average)
		mid = "{:15}".format("Draw: " + draw_odds) # display
		
		# format display
		odds_list = game['away_win']
		sum = 0.0
		counter = 0
		for odds in odds_list:
			sum = sum + odds
			counter = counter + 1
		average = sum/counter 		
		odds_away_win = "{:.2f}".format(average)
		right = "{:25}".format(game['away'] + ": " + odds_away_win) # display
		
		print(left + mid + right)
		
	
def sortData(data):
	
	
data = initData()
data = getSkyBetData(data)		
data = getOddsCheckerData(data)
displayData(data)