import pandas as pd 

def check_if_position_valid(element_type, player_dict):
	if element_type == 1:
		return player_dict[1] < 1
	elif element_type == 2:
		return player_dict[2] < 5
	elif element_type == 3:
		return player_dict[3] < 5
	elif element_type == 4:
		return player_dict[4] < 3
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
	rel_data = data[['web_name', 'id', 'element_type', 'now_cost', 'total_points']].copy()
	rel_data.sort_values(by = 'total_points', inplace = True, ascending = False)
	max_points = 0
	team = []
	max_price = 8300
	for index, player in rel_data.iterrows():
		current_team = []
		current_price = 0
		current_points = 0
		player_types = { 1 : 0, 2:0, 3:0, 4:0}
		for i, n_player in rel_data.iloc[index:].iterrows():
			if not check_if_position_valid(n_player['element_type'], player_types):
				continue
			elif current_price + int(n_player['now_cost']) > max_price:
				continue
			else:
				current_team.append(n_player.to_dict())
				current_price += int(n_player['now_cost'])
				current_points += int(n_player['total_points'])
				if len(current_team) == 11:
					break
		if current_points > max_points and check_team(current_team):
			team = current_team
			max_points = current_points
	team_df = pd.DataFrame(team)
	print(team_df)



if __name__ == "__main__":
	main()