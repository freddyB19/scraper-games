import os
import json

from lol.main import ScraperLOL
from easport.main import ScraperEASport
from noticias.main import ScraperNoticias



BASE = os.path.dirname(os.path.abspath(__file__))

def main():

	results = [
		{'pagina': {'nombre': 'lol', 'info': ScraperLOL.scraper()}},
		{'pagina': {'nombre': 'easport', 'info': ScraperEASport.scraper()}},
		{'pagina': {'nombre': 'noticias', 'info': ScraperNoticias.scraper()}},

	]

	with open(os.path.join(BASE, 'result.json'), 'w+') as file:
		json.dump(results, file, indent=4)
	

if __name__ == '__main__':
	main()