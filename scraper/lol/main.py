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
	'lolnews': 'https://www.leagueoflegends.com/es-es/news/',
	'lolnotas': 'https://www.leagueoflegends.com/es-es/news/tags/patch-notes/',
}


class ScraperLOL:

	@classmethod
	def scraper(cls) -> Dict[str, str]:
		
		champions:Union[str, ResultScraper] = LOLChampionsPage.scrap(
			html_data = ReadFromWeb.read(URLS['lolchampions']),
			url_root = "https://www.leagueoflegends.com"
		)

		noticias:Union[str, ResultScraper] = LOLNewsNotesPage.scrap(html_data = ReadFromWeb.read(URLS['lolnews']))
		notas:Union[str, ResultScraper] = LOLNewsNotesPage.scrap(
			html_data = ReadFromWeb.read(URLS['lolnotas']),
			url_root = "https://www.leagueoflegends.com"
		)

		return {
			'champions': champions,
			'noticias': noticias,
			'notas': notas
		}


def main() -> None:
	pprint.pp(ScraperLOL.scraper(), indent=4)

	
if __name__ == '__main__':
	main()