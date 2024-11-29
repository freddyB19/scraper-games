import os
import json

from lol.main import ScraperLOL
from easport.main import ScraperEASport
from noticias.main import ScraperNoticias



BASE = os.path.dirname(os.path.abspath(__file__))

def main():

	results = [
		{'page': {'name': 'lol', 'info': ScraperLOL.scraper()}},
		{'page': {'name': 'easport', 'info': ScraperEASport.scraper()}},
		{'page': {'name': 'noticias', 'info': ScraperNoticias.scraper()}},

	]

	with open(os.path.join(BASE, 'results', 'result.json'), 'a') as file:
		json.dump(results, file, indent=4)
	

if __name__ == '__main__':
	main()