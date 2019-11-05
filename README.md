# Python Fantasy PL Team Builder
##
Creates a fantasy team using player and team expected goals (xG) data from the previous seasons to predict their expected success. Uses a list of created team difficulties to discretize the level of fixtures, and predicts using the players' upcoming fixtures. 

## Functions 
#### Data Collection
- fpl_load_manual uses the FPL API to create a database of all players in the game and saves as a csv
- get_understat uses a wrapper library to collect xG, expected assists (xA) and expected goals against (xGA) from the understat website and saves as a csv

#### Data Conversion
- merge_understat_fpl merges the two databases collected so that players and teams have their data in a single source. 
- understat_players uses the understat data and adds it to each player class depending on the discretized difficulty of their prior fixtures
- understat_teams uses the understat data and adds it to each team class depending on their fixture history of the previous season
- create_xp creates an expected points measure that calculates the expected points using FPL rules over 10 future fixtures, weighing immediate fixtures more heavily

#### Team Building

- create_team_pulp uses a PuLP optimizer to create the best team possible given the constraints of price of each player, number of players per team, players per position restrictions etc. and calculates the highest possible xP for a team. 

#### Team Position 
- Team position as of 5/11/2019: 15th Percentile