import os
import sys
import pprint
import json


from typing import Dict
from typing import Union
from typing import List
from typing import TypeAlias


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils.main import ReadFromWeb

from lol.pages.lolchampions import LOLChampionsPage 
from lol.pages.lolfandom import LOLFandomPage
from lol.pages.news_and_notes import LOLNewsNotesPage


ResultScraper:TypeAlias = List[Dict[str, str]]

URLS:Dict[str, str] = {
	'lolchampions': 'https://www.leagueoflegends.com/es-es/champions/',
	'lolfandom': 'https://leagueoflegends.fandom.com/es/wiki/Estad%C3%ADsticas_base_de_campeones',
	'lolnews': 'https://www.leagueoflegends.com/es-es/news/',
	'lolnotas': 'https://www.leagueoflegends.com/es-es/news/tags/patch-notes/',
}


# Permite obtener las imagenes de los personajes
def get_champions_img(html):
	columns = html.css.select('table[class*="wikitable"] tr[style!=""]')
	champions = dict()
	for index, column in enumerate(columns[1:]):
		fila = column.td

		url_imagen = fila.find('img').get('data-src')

		imagen_info = url_imagen.partition(".png")

		champions.update({
			fila.find('span', style=True).string.strip(): f"{imagen_info[0]}{imagen_info[1]}" if imagen_info[1] != '' else imagen_info[0]
		})

	return champions


class ScraperLOL:

	@classmethod
	def scraper(cls) -> Dict[str, str]:
		champions_imagen = get_champions_img(html = ReadFromWeb.read(URLS['lolfandom']))
		
		champions:Union[str, ResultScraper] = LOLChampionsPage.scrap(
			html_data = ReadFromWeb.read(URLS['lolchampions']),
			champions_imagen = champions_imagen,
			url_root = "https://www.leagueoflegends.com"
		)

		estadisticas:Union[str, ResultScraper] = LOLFandomPage.scrap(
			html_data = ReadFromWeb.read(URLS['lolfandom']),
			url_root = "https://leagueoflegends.fandom.com"
		)
		noticias:Union[str, ResultScraper] = LOLNewsNotesPage.scrap(html_data = ReadFromWeb.read(URLS['lolnews']))
		notas:Union[str, ResultScraper] = LOLNewsNotesPage.scrap(
			html_data = ReadFromWeb.read(URLS['lolnotas']),
			url_root = "https://www.leagueoflegends.com"
		)

		return {
			'champions': champions,
			'estadisticas': estadisticas,
			'noticias': noticias,
			'notas': notas
		}


def main() -> None:
	pprint.pp(ScraperLOL.scraper(), indent=4)

	
if __name__ == '__main__':
	main()