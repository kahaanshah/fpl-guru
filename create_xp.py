import pandas as pd
from understat_players import Player 
from understat_teams import Team
import pickle

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

if __name__ == "__main__":
	with open('teams_data.pickle', 'rb') as handle:
		teams_dict = pickle.load(handle)
	print(teams_dict)
	for team in teams_dict.values():
		for player in team.players.values():
			player.calc_xp(team)
	fpl_data = pd.read_csv('fpl_data.csv')
	xp_list = []
	for index, player in fpl_data.iterrows():
		try:
			if player['id'] in teams_dict[fpl_to_understat[player['team']]].players:
				xp_list.append(teams_dict[fpl_to_understat[player['team']]].players[player['id']].xp)
			else:
				xp_list.append(0)
		except KeyError:
			xp_list.append(0)
			continue
		
	fpl_data.insert(50, 'xP', xp_list, False)
	fpl_data.to_csv('xP_data.csv')

	
