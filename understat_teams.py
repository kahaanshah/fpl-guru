import pandas as pd
import json 
from understat import Understat 
import asyncio
import aiohttp
import time
import pickle
from understat_players import Player 

if __name__ == "__main__":
	with open('players_xg_xa.pickle', 'rb') as handle:
		players_dict = pickle.load(handle)
	print(players_dict['Arsenal'][2].player)
