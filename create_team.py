import pandas as pd 

formations = [{1:1, 2:3, 3:4, 4:3},
{1:1, 2:3, 3:5, 4:2}, 
{1:1, 2:4, 3:3, 4:3}, 
{1:1, 2:4, 3:4, 4:2}, 
{1:1, 2:4, 3:5, 4:1}, 
{1:1, 2:5, 3:3, 4:2}, 
{1:1, 2:5, 3:4, 4:1}]

def check_if_position_valid(formation, element_type, player_dict):
	if element_type == 1:
		return player_dict[1] < 1
	elif element_type == 2:
		return player_dict[2] < formation[2]
	elif element_type == 3:
		return player_dict[3] < formation[3]
	elif element_type == 4:
		return player_dict[4] < formation[4]
	else:
		raise ValueError("Error occured in check_if_position_valid")

def check_team(team):
	team_dict = { 1 : 0, 2:0, 3:0, 4:0}
	for player in team:
		team_dict[player['element_type']] += 1
	if team_dict[1] > 1 or team_dict[1] < 1:
		return False
	elif team_dict[2] < 3 or team_dict[2] > 5:
		return False
	elif team_dict[3] < 3 or team_dict[3] > 5:
		return False
	elif team_dict[4] < 1 or team_dict[4] > 3:
		return False
	else:
		return True




def main():
	data = pd.read_pickle('data.pkl')
	rel_data = data[['web_name', 'id', 'team', 'element_type', 'now_cost', 'total_points']].copy()
	rel_data.sort_values(by = 'total_points', inplace = True, ascending = False)
	max_points = 0
	team = []
	max_price = 830
	captain_points_final = 0
	for formation in formations:
		for index, player in rel_data.iterrows():
			current_team = []
			current_price = 0
			current_points = 0
			player_types = { 1 : 0, 2:0, 3:0, 4:0}
			team_nums = {team : 0 for team in rel_data['team'].unique()}
			for i, n_player in rel_data.iloc[index:].iterrows():
				if not check_if_position_valid(formation, n_player['element_type'], player_types):
					continue
				if current_price + int(n_player['now_cost']) > max_price:
					continue
				if team_nums[n_player['team']] > 2:
					continue
				else:
					current_team.append(n_player.to_dict())
					player_types[n_player['element_type']] += 1
					team_nums[n_player['team']] += 1
					current_price += int(n_player['now_cost'])
					current_points += int(n_player['total_points'])
					if len(current_team) == 11:
						break
			captain_points = 0
			for i, p in enumerate(current_team):
				if p['total_points'] > captain_points:
					captain_points = p['total_points']
			current_points += captain_points
			if current_points > max_points:
				team = current_team
				max_points = current_points
				captain_points_final = captain_points
	team_df = pd.DataFrame(team)
	team_df.sort_values(by  = 'element_type', inplace = True)
	print(team_df)
	print(captain_points_final)
	print(sum(team_df['now_cost']))
	print(sum(team_df['total_points']))



if __name__ == "__main__":
	main()