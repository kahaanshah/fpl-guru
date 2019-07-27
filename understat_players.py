import pandas as pd
import json 
from understat import Understat 
import asyncio
import aiohttp
import time
import pickle

fpl_to_understat= {1:'Arsenal', 
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
16: 'Southampton',
17: 'Tottenham',
18: 'Watford',
19: 'West Ham',
20: 'Wolverhampton Wanderers'}

intra_transfers= {122 : 'Crystal Palace', 
265 : 'Newcastle United',
205 : 'Manchester City',

}

difficulty = pd.read_csv('EPL_Fixturelist_1920.csv')


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
		self.games_played = {i:0 for i in range(2,6)}
		if self.former_team:
			team = self.former_team
		else:
			team = self.team
		for index, row in understat_data.iterrows():
			if row['h_team'] == team:
				self.xg[difficulty[difficulty['Team'] == row['a_team']]['Home'].values[0]] += row['xG']
				self.xa[difficulty[difficulty['Team'] == row['a_team']]['Home'].values[0]] += row['xA']
				self.games_played[difficulty[difficulty['Team'] == row['a_team']]['Home'].values[0]] += 1

			elif row['a_team'] == team:
				self.xg[difficulty[difficulty['Team'] == row['h_team']]['Away'].values[0]] += row['xG']
				self.xa[difficulty[difficulty['Team'] == row['h_team']]['Away'].values[0]] += row['xA']
				self.games_played[difficulty[difficulty['Team'] == row['h_team']]['Away'].values[0]] += 1
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



def init_players_dict():
	players_dict = dict()
	for value in fpl_to_understat.values():
		players_dict[value] = []
	return players_dict




async def get_player_data(player):
	async with aiohttp.ClientSession() as session:
		understat = Understat(session)
		data_json = await understat.get_player_matches(player_id = player['understat_id'], options = {'season' : '2018'}) 
		data = json.dumps(data_json)
		data_df = pd.read_json(data, orient='records')
		return data_df 




if __name__ == "__main__":
	player_data = pd.read_csv('fpl_data.csv')
	difficulty = pd.read_csv('EPL_Fixturelist_1920.csv')
	players_dict = init_players_dict()
	for index, player in player_data.iloc[340:].iterrows():
		if player['understat_id'] != 0:
			loop = asyncio.get_event_loop()
			player_matches = loop.run_until_complete(get_player_data(player))
			new_player = Player(player)
			try:
				new_player.calculate_xg_xa(player_matches)
			except ValueError:
				print(player)
				continue
			players_dict[fpl_to_understat[player['team']]].append(new_player)
		print(index)
	print(players_dict)
	with open('players_xg_xa.pickle', 'wb') as handle:
		pickle.dump(players_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
	



