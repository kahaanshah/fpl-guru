from trial import Data
import aiohttp
import asyncio


async def save_player():
	async with aiohttp.ClientSession() as session:
		fpl = Data(session)
		players = await fpl.get_players()
		print(players)
			

asyncio.run(save_player())