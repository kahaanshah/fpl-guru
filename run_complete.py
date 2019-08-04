import fpl_load_manual
import get_understat
import merge_understat_fpl
import understat_players
import understat_teams
import create_xp
import create_team_pulp
import create_team_random

if __name__ == "__main__":
	fpl_load_manual.run_fpl_load_manual()
	get_understat.run_get_understat()
	merge_understat_fpl.main()
	understat_players.main()
	understat_teams.main()
	create_xp.main()
	create_team_pulp.main()
	#create_team_random.main
