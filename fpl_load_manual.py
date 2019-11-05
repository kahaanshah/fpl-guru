import time
import json 
import requests
import pandas as pd

API_URL = "https://fantasy.premierleague.com/api/"

API_URLS = {
	"dynamic" : "{}bootstrap-dynamic".format(API_URL),
	"static" : "{}bootstrap-static".format(API_URL),
	"players" : "{}elements".format(API_URL),
	"team" : "{}my-team/2226961".format(API_URL)
}

def get_data():
	r = ''
	while r == '':
		try:
			r = requests.get(API_URLS['static'])
		except (KeyboardInterrupt, SystemExit) as r:
			raise
		except Exception as e:
			print(e)
			time.sleep(5)
			continue
	data = json.dumps((r.json()["elements"]))
	data_df = pd.read_json(data, orient = 'records')
	return data_df

def run_fpl_load_manual():
	data = get_data()
	data.to_csv('data.csv')
	data.to_pickle("data.pkl")

if __name__ == "__main__":
	run_fpl_load_manual()