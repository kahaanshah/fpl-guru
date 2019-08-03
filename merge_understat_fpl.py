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
		is_same = (understat_data['player_name'].str.contains(name))
		common = understat_data[is_same]
		if len(common) == 1:
			id_list.append(common['id'].values[0])
			continue
		is_same = ((understat_data['first_name'].str.contains(first_name)) & 
			understat_data['last_name'].str.contains((last_name)))
		common = understat_data[is_same]
		if len(common)>1:
			is_same = (understat_data['first_name'].str.contains(first_name) & 
				understat_data['team_title'].str.contains(team) &
				understat_data['last_name'].str.contains(last_name))
			common = understat_data[is_same]
		elif len(common) == 0:
			is_same = (understat_data['first_name'].str.contains(first_name) &
				understat_data['team_title'].str.contains(team))
			common = understat_data[is_same]
		if len(common) != 1:
			id_list.append(0)
		else:
			id_list.append(common['id'].values[0])
	return id_list


def main():
	fpl_data = pd.read_csv('data.csv')
	understat_data = pd.read_csv('understat.csv')
	first_name = []
	last_name = []
	for index, row in understat_data.iterrows():
		names = row['player_name'].split()
		first_name.append(names[0])
		try:
			last_name.append(names[1]+names[2])
		except IndexError:
			try:
				last_name.append(names[1])
			except IndexError:
				last_name.append('')
	understat_data.insert(2, 'first_name', first_name, False)
	understat_data.insert(3, 'last_name', last_name, False)
	id_list = merge_data(fpl_data, understat_data)
	fpl_data.insert(49, 'understat_id', id_list, False)
	fpl_data.to_csv('fpl_data.csv')
		

if __name__ == "__main__":
	main()