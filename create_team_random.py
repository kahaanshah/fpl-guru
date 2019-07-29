import pandas as pd 
import random
import time
import multiprocessing as mp 

class Fantasy_Team():

	def __init__(self, players = None):
		self.team = []
		self.player_set = set()
		self.now_cost = 0
		self.points = 0
		self.team_dict = {i:0 for i in range(1, 21)}
		self.position_dict = {i:0 for i in range(1,5)}
		self.captain_points = 0
		if players:
			for player in players:
				self.add_player(player)
		

	def check_value(self, player):
		players_left = 11- len(self.team)
		if players_left < 7:
			if (players_left-1) * 45 + self.now_cost + player['now_cost'] > 830:
				return False
			else:
				return True
		else:
			return True

	def check_position(self, player):
		if player['element_type'] == 1:
			return self.position_dict[1] < 1
		if player['element_type'] == 2:
			return self.position_dict[2] < 5
		if player['element_type'] == 3:
			return self.position_dict[3] < 5
		if player['element_type'] == 4:
			return self.position_dict[4] < 3
 

	def valid_player(self, player):
		if player['id'] in self.player_set:
			return False
		elif player['now_cost'] + self.now_cost > 830:
			return False
		elif len(self.team) >= 11:
			return False
		elif self.team_dict[player['team']] > 2:
			return False
		elif not self.check_value(player):
			return False
		elif not self.check_position(player):
			return False
		else:
			return True

	def substitute_player(self, player):
		for index, p in enumerate(self.team):
			if p['element_type'] == player['element_type']:
				if player['id'] in self.player_set:
					continue
				if p['xP'] > player['xP']:
					continue
				if (player['now_cost'] - p['now_cost']) + self.now_cost > 830:
					continue
				if player['team'] == p['team']:
					self.do_substitution(index, p, player)
				elif self.team_dict[player['team']] < 3:
					self.do_substitution(index, p, player)
			else: 
				continue

	def do_substitution(self, i_out, player_out, player_in):
		self.now_cost -= player_out['now_cost']
		self.player_set.remove(player_out['id'])
		self.points -= player_out['xP']
		self.team_dict[player_out['team']] -= 1
		self.position_dict[player_out['element_type']] -= 1
		if player_out['xP'] == self.captain_points:
			captain_points = 0
			for high_player in self.team:
				if high_player['xP'] > captain_points:
					captain_points = high_player['xP']
			self.points -= self.captain_points
			self.captain_points = captain_points
			self.points += self.captain_points
		del self.team[i_out]
		self.add_player(player_in)

	
	def add_player(self, player):
		self.team.append(player)
		self.now_cost += player['now_cost']
		self.player_set.add(player['id'])
		self.points += player['xP']
		self.team_dict[player['team']] += 1
		self.position_dict[player['element_type']] += 1
		if player['xP'] > self.captain_points:
			self.points -= self.captain_points
			self.captain_points = player['xP']
			self.points += self.captain_points


	def team_valid(self):
		if len(self.team) != 11:
			return False
		elif self.position_dict[1] != 1:
			return False
		elif self.position_dict[2] < 3:
			return False
		elif self.position_dict[4] < 1:
			return False
		else:
			return True

	def __repr__(self):
		team_df = pd.DataFrame(self.team)
		team_df.sort_values(by  = 'element_type', inplace = True)
		return team_df.to_string()


def create_random_team(players):
	new_team = Fantasy_Team()
	while(not new_team.team_valid()):
		new_team = Fantasy_Team()
		while(len(new_team.team) < 11):
			rand = random.randint(0, len(players)-1)
			if new_team.valid_player(players.iloc[rand]):
				new_team.add_player(players.iloc[rand])
	return new_team

def make_team_better(team, sorted_data):
	for player in sorted_data:
		team.substitute_player(player)
	return team

def func(data, num, return_dict):
	sorted_data = data.sort_values(by = 'xP', inplace = False, ascending = False)
	max_points = 0
	max_team = None
	for i in range(num):
		team = create_random_team(data)
		sorted_data = sorted_data.sample(frac=1).reset_index(drop = True)
		for index, p in sorted_data.iterrows():
			#if p['xP'] < team.low_player_points:
				#break
			team.substitute_player(p)
		if team.points >  max_points:
			max_points = team.points
			max_team = team
		
	return_dict[max_points] = max_team
	return (max_team, max_points)
	
def main():
	data = pd.read_csv('xP_data.csv')
	data = data[data['minutes']>1500]
	for i in range(10):
		data_temp = data[['web_name', 'id', 'team', 'element_type', 'now_cost', 'GW'+str(i)]].copy()
		data_temp.rename(columns = {'GW'+str(i) : 'xP'}, inplace = True)
		manager = mp.Manager()
		return_dict = manager.dict()
		jobs = []
		for _ in range(4):
			p = mp.Process(target = func, args = (data_temp, 250, return_dict))
			jobs.append(p)
			p.start()
		for job in jobs:
			job.join()
		print(return_dict[max(return_dict.keys())])
		print(max(return_dict.keys()))
		print(return_dict[max(return_dict.keys())].now_cost)

if __name__ == "__main__":
	main()
	






