import aiohttp
import asyncio
from fpl import FPL
from fpl.constants import API_URLS
from fpl.utils import fetch


class Data():

	def __init__(self, session):
		self.session = session

	async def get_players(self):
		players = await fetch(self.session, API_URLS["static"])
		print(players)
		return players




