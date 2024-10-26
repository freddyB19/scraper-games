from typing import Dict
from typing import Union
from typing import List
from typing import TypeAlias


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

class ScraperLOL:

	@classmethod
	def scraper(cls) -> Dict[str, str]:
		champions:Union[str, ResultScraper] = LOLChampionsPage.scrap(html_data = ReadFromWeb.read(URLS['lolchampions']))
		estadisticas:Union[str, ResultScraper] = LOLFandomPage.scrap(html_data = ReadFromWeb.read(URLS['lolfandom']))
		noticias:Union[str, ResultScraper] = LOLNewsNotesPage.scrap(html_data = ReadFromWeb.read(URLS['lolnews']))
		notas:Union[str, ResultScraper] = LOLNewsNotesPage.scrap(html_data = ReadFromWeb.read(URLS['lolnotas']))

		return {
			'champions': champions,
			'estadisticas': estadisticas,
			'noticias': noticias,
			'notas': notas
		}

def main() -> None:
	ScraperLOL.scraper()

if __name__ == '__main__':
	main()