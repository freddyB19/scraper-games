import os, sys, pprint

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils.main import ReadFromWeb

from lol.pages.lolchampions import LOLChampionsPage 
from lol.pages.lolfandom import LOLFandomPage
from lol.pages.news_and_notes import LOLNewsNotesPage


URLS = {
	'lolchampions': 'https://www.leagueoflegends.com/es-es/champions/',
	'lolnews': 'https://www.leagueoflegends.com/es-es/news/',
	'lolnotas': 'https://www.leagueoflegends.com/es-es/news/tags/patch-notes/',
}


class ScraperLOL:

	@classmethod
	def scraper(cls) -> dict[str, list[dict[str, str]] | None]:
		
		champions = LOLChampionsPage.scrap(
			html_data = ReadFromWeb.read(URLS['lolchampions']),
			url_root = "https://www.leagueoflegends.com"
		)

		noticias = LOLNewsNotesPage.scrap(html_data = ReadFromWeb.read(URLS['lolnews']))
		notas = LOLNewsNotesPage.scrap(
			html_data = ReadFromWeb.read(URLS['lolnotas']),
			url_root = "https://www.leagueoflegends.com"
		)

		return {
			'champions': champions,
			'noticias': noticias,
			'notas': notas
		}


def main() -> None:
	pprint.pprint(ScraperLOL.scraper(), indent=4)

	
if __name__ == '__main__':
	main()
