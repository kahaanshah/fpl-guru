import pandas as pd
from pulp import *
import re

formations = [{1:1, 2:3, 3:4, 4:3},
{1:1, 2:3, 3:5, 4:2}, 
{1:1, 2:4, 3:3, 4:3}, 
{1:1, 2:4, 3:4, 4:2}, 
{1:1, 2:4, 3:5, 4:1}, 
{1:1, 2:5, 3:3, 4:2}, 
{1:1, 2:5, 3:4, 4:1}]

def main():
	data = pd.read_csv('xP_data.csv')
	data = data[(data['chance_of_playing_next_round'] != 0) &
		(data['chance_of_playing_next_round'] != 25) &
		(data['chance_of_playing_next_round'] != 50) &
		(data['chance_of_playing_next_round'] != 75)]
	data = data[['web_name', 'id', 'team', 'element_type', 'now_cost', 'minutes', 'Aggregate_xp']].copy()
	data = data[data['minutes']>1500].reset_index()
	teams_returned = []
	for formation in formations:
		create_problem(formation, data, teams_returned)
	max_value = max([team[0] for team in teams_returned])
	for value, team in teams_returned:
		if value == max_value:
			print(value)
			print(team)



def create_problem(formation, data, return_list):
	num_gks = formation[1]
	num_defs = formation[2]
	num_mids = formation[3]
	num_fwds = formation[4]

	prob = pulp.LpProblem('FPL_team', pulp.LpMaximize)
	decision_variables = []
	for rownum, row in data.iterrows():
		player = str('p'+str(rownum))
		player = pulp.LpVariable(str(player), lowBound = 0, upBound = 1, cat = 'Integer')
		decision_variables.append(player)

	total_points = ""

	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum==i:
				formula = row['Aggregate_xp']*player
				total_points += formula
	prob += total_points


	avail_cash = 830
	total_paid = ""
	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum == i:
				formula = row['now_cost']*player
				total_paid += formula
	prob += (total_paid <= avail_cash)

	avail_gk = num_gks
	total_gk = ""
	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum == i:
				if row['element_type'] == 1:
					formula = 1*player
					total_gk += formula
	prob += (total_gk == avail_gk)
	#print(total_gk)

	avail_def = num_defs
	total_def = ""
	for rownum, row in data.iterrows():
		for i,player in enumerate(decision_variables):
			if rownum == i:
				if row['element_type'] == 2:
					formula = 1*player
					total_def += formula
	prob += (total_def == avail_def)
	#print(total_def)

	avail_mid = num_mids
	total_mid = ""
	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum == i:
				if row['element_type'] == 3:
					formula = 1*player
					total_mid += formula
	prob += (total_mid == avail_mid)
	#print((total_mid))

	avail_fwd = num_fwds
	total_fwd = ""
	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum == i:
				if row['element_type'] == 4:
					formula = 1*player
					total_fwd += formula
	prob += (total_fwd == avail_fwd)
	#print(total_fwd)

	team_dict = {}
	for team in set(data.team):
		team_dict[str(team)] = dict()
		team_dict[str(team)]['avail'] = 3
		team_dict[str(team)]['total'] = ""
		for rownum, row in data.iterrows():
			for i, player in enumerate(decision_variables):
				if rownum == i:
					if row['team'] == team:
						formula = 1*player
						team_dict[str(team)]['total'] += formula
		prob += (team_dict[str(team)]['total'] <= team_dict[str(team)]['avail'])
	#print(team_dict)

	prob.writeLP('fpl_team.lp')
	optimization_result = prob.solve()
	assert optimization_result == pulp.LpStatusOptimal
	print('Status: ', LpStatus[prob.status])
	print('Optimal Solution', pulp.value(prob.objective))
	#print('Individual decision_variables: ')
	#for v in prob.variables():
		#print(v.name, '=', v.varValue)

	variable_name = []
	variable_value = []
	for v in prob.variables():
		variable_name.append(v.name)
		variable_value.append(v.varValue)

	df = pd.DataFrame({'variable' : variable_name, 'value':variable_value})
	for rownum, row in df.iterrows():
		value = re.findall(r'(\d+)', row['variable'])
		df.loc[rownum, 'variable'] = int(value[0])

	df.sort_index(by = 'variable')

	for rownum, row in data.iterrows():
		for results_rownum, results_row in df.iterrows():
			if rownum == results_row['variable']:
				data.loc[rownum, 'decision'] = results_row['value']

	return_list.append((data[data.decision==1].Aggregate_xp.sum(), data[data.decision == 1].sort_values('element_type')))
	#print(data[data.decision==1].now_cost.sum())
	#print(data[data.decision==1].Aggregate_xp.sum())
	#print(data[data.decision == 1].sort_values('element_type'))



if __name__ == "__main__":
	main()