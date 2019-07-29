import pandas as pd 
from multiprocessing import Pool


formations = [{1:1, 2:3, 3:4, 4:3},
{1:1, 2:3, 3:5, 4:2}, 
{1:1, 2:4, 3:3, 4:3}, 
{1:1, 2:4, 3:4, 4:2}, 
{1:1, 2:4, 3:5, 4:1}, 
{1:1, 2:5, 3:3, 4:2}, 
{1:1, 2:5, 3:4, 4:1}]

class Team():

	def __init__(self, players = None):
		self.team = []
		self.player_set = set()
		self.now_cost = 0
		self.points = 0
		self.team_dict = {i:0 for i in range(1, 21)}
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
		else:
			return True
	
	def add_player(self, player):
		self.team.append(player)
		self.now_cost += player['now_cost']
		self.player_set.add(player['id'])
		self.points += player['total_points']
		self.team_dict[player['team']] += 1

	def team_valid(self):
		if len(self.team == 11):
			return True
		else:
			return False

	def __repr__(self):
		team_df = pd.DataFrame(self.team)
		team_df.sort_values(by  = 'element_type', inplace = True)
		return team_df.to_string()




def main():
	data = pd.read_pickle('data.pkl')
	rel_data = data[['web_name', 'id', 'team', 'element_type', 'now_cost', 'total_points']].copy()
	rel_data.sort_values(by = 'total_points', inplace = True, ascending = False)
	gks = rel_data[rel_data['element_type'] == 1]
	gks = gks[gks['total_points'] > 100]
	defs = rel_data[rel_data['element_type'] == 2]
	defs = defs[defs['total_points']>150]
	mids = rel_data[rel_data['element_type'] == 3]
	mids = mids[mids['total_points']>150]
	att = rel_data[rel_data['element_type'] == 4]
	att = att[att['total_points']>150]
	players_dict = {1:gks, 2:defs, 3:mids, 4:att}
	max_team_points = 0
	max_team = None
	for i, gk in gks.iloc[:5].iterrows():
		current_team = Team()
		current_team.add_player(gk)
		def_count = 0
		players_so_far = []
		print(gk)
		for i, p2 in defs.iterrows():
			print(p2)
			if current_team.valid_player(p2):
				current_team.add_player(p2)
			else:
				continue
			for i, p3 in defs.iterrows():
				print(p3)
				if current_team.valid_player(p3):
					current_team.add_player(p3)
				else:
					continue
				for i, p4 in defs.iterrows():
					print(p4)
					if current_team.valid_player(p4):
						current_team.add_player(p4)
					else:
						continue
					for i, p5 in defs.iterrows():
						print(p5)
						if current_team.valid_player(p5):
							current_team.add_player(p5)
						else:
							continue
						for i, p6 in mids.iterrows():
							print(p6)
							if current_team.valid_player(p6):
								current_team.add_player(p6)
							else:
								continue
							for i, p7 in mids.iterrows():
								if current_team.valid_player(p7):
									current_team.add_player(p7)
								else:
									continue
								for i, p8 in mids.iterrows():
									if current_team.valid_player(p8):
										current_team.add_player(p8)
									else:
										continue
									for i, p9 in mids.iterrows():
										if current_team.valid_player(p9):
											current_team.add_player(p9)
										else:
											continue
										for i, p10 in att.iterrows():
											if current_team.valid_player(p10):
												current_team.add_player(p10)
											else:
												continue
											for i, p11 in att.iterrows():
												if current_team.valid_player(p11):
													current_team.add_player(p11)
												else:
													continue
												if current_team.points > max_team_points:
														print(current_team)
														print(current_team.points)
														max_team = current_team
														max_team_points = current_team.points	
												current_team= Team([gk, p2, p3, p4, p5, p6, p7, p8, p9, p10])
											current_team= Team([gk, p2, p3, p4, p5, p6, p7, p8, p9])
										current_team= Team([gk, p2, p3, p4, p5, p6, p7, p8])
									current_team= Team([gk, p2, p3, p4, p5, p6, p7])
								current_team= Team([gk, p2, p3, p4, p5, p6])
							current_team= Team([gk, p2, p3, p4, p5])
						current_team= Team([gk, p2, p3, p4])
					current_team= Team([gk, p2, p3])
				current_team= Team([gk, p2])			
			current_team = Team([gk])



															
												
	print(max_team)
	print(max_team_points)




if __name__ == "__main__":
	main()