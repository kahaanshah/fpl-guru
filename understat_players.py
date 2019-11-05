import pandas as pd
import json 
from understat import Understat 
import asyncio
import aiohttp
import time
import pickle
import copy



fpl_to_understat= {1:'Arsenal', 
2: 'Aston Villa',
3:'Bournemouth',
4: 'Brighton',
5: 'Burnley',
6: 'Chelsea',
7: 'Crystal Palace',
8: 'Everton',
9: 'Leicester',
10: 'Liverpool',
11: 'Manchester City',
12: 'Manchester United',
13: 'Newcastle United',
14: 'Norwich',
15: 'Sheffield United',
16: 'Southampton',
17: 'Tottenham',
18: 'Watford',
19: 'West Ham',
20: 'Wolverhampton Wanderers'}

intra_transfers= {122 : 'Crystal Palace', 
265 : 'Newcastle United',
205 : 'Manchester City',
106 : 'Chelsea'
}

difficulty = pd.read_csv('EPL_Fixturelist_1920.csv')

team_games_played = dict()

def get_team_games_played(team):
	games_played = {i:0 for i in range(2,6)}
	for index, row in difficulty.iterrows():
		if row['Team'] == team:
			continue
		else:
			games_played[row['Home']] += 1
			games_played[row['Away']] += 1
	return games_played

class Player():

	def __init__(self, fpl_data):
		self.player = fpl_data
		self.team = fpl_to_understat[fpl_data['team']]
		try:
			self.former_team = intra_transfers[self.player['id']]
		except KeyError:
			self.former_team = None

	def calculate_xg_xa(self, understat_data):
		self.xg = {i:0 for i in range(2,6)}
		self.xa = {i:0 for i in range(2,6)}
		try:
			self.games_played = copy.deepcopy(team_games_played[self.team])
		except KeyError:
			gp = get_team_games_played(self.team)
			team_games_played[self.team] = gp
			self.games_played = copy.deepcopy(team_games_played[self.team])
		self.minutes_played = {i:0 for i in range(2,6)}
		if self.former_team:
			team = self.former_team
		else:
			team = self.team
		for index, row in understat_data.iterrows():
			if row['h_team'] == team:
				self.xg[difficulty[difficulty['Team'] == row['a_team']]['Home'].values[0]] += row['xG']
				self.xa[difficulty[difficulty['Team'] == row['a_team']]['Home'].values[0]] += row['xA']
				self.minutes_played[difficulty[difficulty['Team'] == row['a_team']]['Home'].values[0]] += row['time']
				if row['season'] == 2019:
					self.games_played[difficulty[difficulty['Team'] == row['a_team']]['Home'].values[0]] += 1
			elif row['a_team'] == team:
				self.xg[difficulty[difficulty['Team'] == row['h_team']]['Away'].values[0]] += row['xG']
				self.xa[difficulty[difficulty['Team'] == row['h_team']]['Away'].values[0]] += row['xA']
				self.minutes_played[difficulty[difficulty['Team'] == row['h_team']]['Away'].values[0]] += row['time']
				if row['season'] == 2019:
					self.games_played[difficulty[difficulty['Team'] == row['a_team']]['Home'].values[0]] += 1
			else: 
				continue
				
		for key in self.xg:
			try:
				self.xg[key] = self.xg[key]/self.games_played[key]
				self.xa[key] = self.xa[key]/self.games_played[key]
			except ZeroDivisionError:
				if self.xg[key] > 0 or self.xa[key] > 0:
					print(self.xg[key], self.xa[key])
					raise ValueError
				else:
					continue


	def add_xga(self, xga):
		self.xga = xga

	def calc_xp(self, fixture_num, team_data, injury_status):
		fixture = team_data.fixtures[fixture_num]
		if pd.isna(injury_status):
			injury_status = 100
		if self.player['element_type'] == 1 or self.player['element_type'] == 2:
			xgp = self.xg[fixture] * 6
			xap = self.xa[fixture] * 3
			xgap = xga_to_xp(self.xga[fixture])
			self.xp = (xgp + xap + xgap + 2) * (injury_status/100)
		elif self.player['element_type'] == 3:
			xgp = self.xg[fixture] * 5 
			xap = self.xg[fixture] * 3
			xga_f = xga_to_xp(self.xga[fixture])
			if xga_f > 1:
				xgap = 0
			else:
				xgap = 1-xga_f
			self.xp = (xgp + xap + xgap + 2) * (injury_status/100)
		elif self.player['element_type'] == 4:
			xgp = self.xg[fixture] * 4
			xap = self.xg[fixture] * 3
			self.xp = (xgp + xap + 2) * (injury_status/100)
		return self.xp


def xga_to_xp(xga):
	return 0.0258*(xga**4) - 0.4035*(xga**3) + 2.2435*(xga*xga) - 5.072*xga + 4.1468


def init_players_dict():
	players_dict = dict()
	for value in fpl_to_understat.values():
		players_dict[value] = dict()
	return players_dict




async def get_player_data(player):
	async with aiohttp.ClientSession() as session:
		understat = Understat(session)
		data_json = await understat.get_player_matches(player)
		data = json.dumps(data_json)
		data_df = pd.read_json(data, orient='records')
		data_df = data_df[data_df['season']>=2018]
		return data_df 



def main():
	player_data = pd.read_csv('fpl_data.csv')
	difficulty = pd.read_csv('EPL_Fixturelist_1920.csv')
	players_dict = init_players_dict()
	for index, player in player_data.iterrows():
		if player['understat_id'] != 0:
			loop = asyncio.get_event_loop()
			player_matches = loop.run_until_complete(get_player_data(player['understat_id']))
			new_player = Player(player)
			try:
				new_player.calculate_xg_xa(player_matches)
			except ValueError:
				print(player)
				continue
			players_dict[fpl_to_understat[player['team']]][player['id']] = new_player
		print(index)
	print(players_dict)
	with open('players_xg_xa.pickle', 'wb') as handle:
		pickle.dump(players_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
	
if __name__ == "__main__":
	main()
	
