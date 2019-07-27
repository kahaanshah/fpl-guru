import pandas as pd

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

def merge_data(fpl_data, understat_data):
	id_list = []
	for index, player in fpl_data.iterrows():
		name = player['web_name']
		try:
			team = fpl_to_understat[player['team']]
		except KeyError:
			id_list.append(0)
			continue
		first_name = player['first_name']
		last_name = player['second_name']
		is_same = (understat_data['player_name'].str.contains(name) & understat_data['team_title'].str.contains(team))
		common = understat_data[is_same]
		if len(common)<1:
			is_same = (understat_data['player_name'].str.contains(first_name) & understat_data['player_name'].str.contains(last_name))
			common = understat_data[is_same]
		if len(common)<1:
			id_list.append(0)
		else:
			id_list.append(common['id'].values[0])
	return id_list


def main():
	fpl_data = pd.read_csv('data.csv')
	understat_data = pd.read_csv('understat.csv')
	id_list = merge_data(fpl_data, understat_data)
	fpl_data.insert(49, 'understat_id', id_list, False)
	fpl_data.to_csv('fpl_data.csv')
		

if __name__ == "__main__":
	main()