import json 
import requests
import asyncio
import aiohttp
from understat import Understat 
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


async def main():
	async with aiohttp.ClientSession() as session:
		understat = Understat(session)
		data_json = await understat.get_league_players('epl', 2019)
		data = json.dumps(data_json)
		data_df = pd.read_json(data, orient='records')
		data_df.to_csv('understat.csv')
		data_df.to_pickle('data.pkl')

def run_get_understat():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

if __name__ == "__main__":
	run_get_understat()