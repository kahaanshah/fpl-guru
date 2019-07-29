import pandas as pd
import json 
from understat import Understat 
import asyncio
import aiohttp
import time
import pickle
from understat_players import Player 
import requests

API_URL = "https://fantasy.premierleague.com/api/fixtures/"

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

difficulty = pd.read_csv('EPL_Fixturelist_1920.csv')

class Team():

	def __init__(self, team, players):
		self.club = team
		self.players = players
		player_list = list(players.values())
		self.team_num = player_list[0].player['team']

	def calculate_xg_xga(self, understat_data):
		self.xg_for = {i:0 for i in range(2,6)}
		self.xga = {i:0 for i in range(2,6)}
		self.games_played = {i:0 for i in range(2,6)}
		for index, row in understat_data.iterrows():
			if row['side'] == 'h':
				self.xg_for[difficulty[difficulty['Team'] == row['a']['title']]['Home'].values[0]] += float(row['xG']['h'])
				self.xga[difficulty[difficulty['Team'] == row['a']['title']]['Home'].values[0]] += float(row['xG']['a'])
				self.games_played[difficulty[difficulty['Team'] == row['a']['title']]['Home'].values[0]] += 1
			elif row['side'] == 'a':
				self.xg_for[difficulty[difficulty['Team'] == row['h']['title']]['Away'].values[0]] += float(row['xG']['a'])
				self.xga[difficulty[difficulty['Team'] == row['h']['title']]['Away'].values[0]] += float(row['xG']['h'])
				self.games_played[difficulty[difficulty['Team'] == row['h']['title']]['Away'].values[0]] += 1
			else:
				raise ValueError('Team not found')
		for key in self.xg_for:
			self.xg_for[key] = self.xg_for[key]/self.games_played[key]
			self.xga[key] = self.xga[key]/self.games_played[key]
		self.xga_to_players()

	def xga_to_players(self):
		for player in self.players.values():
			player.add_xga(self.xga)

	def add_fixtures(self, fixture_list):
		self.fixtures = []
		for i, fixture in fixture_list.iterrows():
			if fixture['team_h'] == self.team_num:
				self.fixtures.append(difficulty[difficulty['Team'] ==  fpl_to_understat[fixture['team_a']]]['Home'].values[0])
			elif fixture['team_a'] == self.team_num:
				self.fixtures.append(difficulty[difficulty['Team'] ==  fpl_to_understat[fixture['team_h']]]['Away'].values[0])
			else:
			 	continue




def get_fixtures():
	r = requests.get(API_URL)
	data = json.dumps(r.json())
	data_df = pd.read_json(data, orient = 'records')
	data_df.to_csv('fixtures_list.csv')
	return data_df


async def get_team_data(team):
	async with aiohttp.ClientSession() as session:
		understat = Understat(session)
		team_json = await understat.get_team_results(team, '2018')
		data = json.dumps(team_json)
		data_df = pd.read_json(data, orient='records')
		return data_df

def main():
	with open('players_xg_xa.pickle', 'rb') as handle:
		players_dict = pickle.load(handle)
	loop = asyncio.get_event_loop()
	teams = dict()
	fixtures = get_fixtures()
	for team in players_dict.keys():
		team_matches = loop.run_until_complete(get_team_data(team))
		new_team = Team(team, players_dict[team])
		new_team.calculate_xg_xga(team_matches)
		new_team.add_fixtures(fixtures)
		teams[team] = new_team
		print(team)
	with open('teams_data.pickle', 'wb') as handle:
		pickle.dump(teams, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
	main()









