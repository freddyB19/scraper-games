import os, sys, json, pprint

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils.main import ReadFromFile, ReadFromWeb, DownloadFile

from easport.pages.noticias import NoticiasEASport
from easport.pages.novedades import NovedadesEASport
from easport.pages.gratuitos import JuegoGratuitosEASport
from easport.pages.proximamente import ProximamenteEASport
from easport.pages.actualizaciones import ActualizacionesEASport


URL = {
	'easport': 'https://www.ea.com/es-es',
	'noticias': 'https://www.ea.com/es-es/news',
	'novedades': 'https://www.ea.com/es-es/games',
	'proximamente' : 'https://www.ea.com/es-es/games/coming-soon',
	'gratuitos': 'https://www.ea.com/es-es/games/library/freetoplay'
}

def easport_news() -> list[dict[str, str | None]] | None:
	noticias = NoticiasEASport.scrap(
		html_data = ReadFromFile.read("./scraper/easport/noticias.html")
	)

	return noticias

def easport_novelties():
	ROOT = 'https://www.ea.com'
	novedades = NovedadesEASport.scrap(
		html_data = ReadFromFile.read("./scraper/easport/novedades.html"),
		url_root = ROOT
	)

	return novedades

def easport_soon():
	proximamente = ProximamenteEASport.scrap(
		html_data = ReadFromFile.read("./scraper/easport/proximamente.html")
	)

	return proximamente

def easport_free():
	ROOT = 'https://www.ea.com'

	gratuitos = JuegoGratuitosEASport.scrap(
		html_data = ReadFromFile.read("./scraper/easport/gratuitos.html"),
		url_root = ROOT
	)

	return gratuitos

def easport_updates():
	actualizaciones = ActualizacionesEASport.scrap(
		html_data = ReadFromFile.read("./scraper/easport/actualizaciones.html")
	)

	return actualizaciones


class ScraperEASport:

	@classmethod
	def scraper(cls):
		data_news = easport_news()
		data_novelties = easport_novelties()
		data_soon = easport_soon()
		data_free = easport_free()
		data_updates = easport_updates()
		
		return {
			'noticias': data_news,
			'novedades': data_novelties,
			'proximamente': data_soon,
			'gratuitos': data_free,
			'actualizaciones': data_updates,
		}

def main():
	pprint.pprint(ScraperEASport.scraper(), indent = 4)


if __name__ == '__main__':
	main()