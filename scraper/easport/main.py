import os
import sys
import json
from typing import Dict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils.main import ReadFromFile
from utils.main import ReadFromWeb

from easport.pages.noticias import NoticiasEASport
from easport.pages.novedades import NovedadesEASport
from easport.pages.gratuitos import JuegoGratuitosEASport
from easport.pages.proximamente import ProximamenteEASport
from easport.pages.actualizaciones import ActualizacionesEASport


URL:Dict[str, str] = {
	'easport': 'https://www.ea.com/es-es',
	'noticias': 'https://www.ea.com/es-es/news',
	'novedades': 'https://www.ea.com/es-es/games',
	'proximamente' : 'https://www.ea.com/es-es/games/coming-soon',
	'gratuitos': 'https://www.ea.com/es-es/games/library/freetoplay'
}

class ScraperEASport:

	@classmethod
	def scraper(cls):
		noticias = NoticiasEASport.scrap(
			html_data = ReadFromWeb.read(url = URL['noticias'])
		)

		novedades = NovedadesEASport.scrap(
			html_data = ReadFromWeb.read(url = URL['novedades'])
		)

		proximamente = ProximamenteEASport.scrap(
			html_data = ReadFromWeb.read(url = URL['proximamente'])
		)
		
		gratuitos = JuegoGratuitosEASport.scrap(
			html_data = ReadFromWeb.read(url = URL['gratuitos'])
		)
		
		actualizaciones = ActualizacionesEASport.scrap(
			html_data = ReadFromWeb.read(url = URL['easport'])
		)

		return {
			'noticias': noticias,
			'novedades': novedades,
			'proximamente': proximamente,
			'gratuitos': gratuitos,
			'actualizaciones': actualizaciones,
		}

def main():
	ScraperEASport.scraper()

if __name__ == '__main__':
	main()