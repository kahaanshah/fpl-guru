import aiohttp
import asyncio
from fpl import FPL
import pickle

async def save_player():
	async with aiohttp.ClientSession() as session:
		fpl = FPL(session)
		players = await fpl.get_players()
		with open('player_data.pkl', 'wb') as output:
			pickle.dump(players, output, pickle.HIGHEST_PROTOCOL)

asyncio.run(save_player())

