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



def main():
	with open('teams_data.pickle', 'rb') as handle:
		teams_dict = pickle.load(handle)
	fpl_data = pd.read_csv('fpl_data.csv')
	xp_dict = {('GW' + str(i)):list() for i in range(10)}
	aggregate_xp = []
	for index, player in fpl_data.iterrows():
		aggregate_sum = 0
		try:
			if player['id'] in teams_dict[fpl_to_understat[player['team']]].players:
				for num in range(10):
					xp = teams_dict[fpl_to_understat[player['team']]].players[player['id']].calc_xp(num, teams_dict[fpl_to_understat[player['team']]])
					aggregate_sum += (xp*(11-num))/65
					xp_dict['GW'+str(num)].append(xp)
				aggregate_xp.append(aggregate_sum)
			else:
				for num in range(10):
					xp_dict['GW'+str(num)].append(0)
				aggregate_xp.append(0)
		except KeyError:
			for num in range(10):
				xp_dict['GW'+str(num)].append(0)
			aggregate_xp.append(0)
			continue
	for gw in xp_dict.keys():
		fpl_data.insert(50, gw, xp_dict[gw], False)
	fpl_data.insert(10, 'Aggregate_xp', aggregate_xp, False)
	fpl_data.to_csv('xP_data.csv')

if __name__ == "__main__":
	main()
	

	
