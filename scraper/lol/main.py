
from utils.main import ReadFromWeb
from lol.pages.lolchampions import LOLChampionsPage 
from lol.pages.lolfandom import LOLFandomPage
from lol.pages.news_and_notes import LOLNewsNotesPage


URLS:dict = {
	'lolchampions': 'https://www.leagueoflegends.com/es-es/champions/',
	'lolfandom': 'https://leagueoflegends.fandom.com/es/wiki/Estad%C3%ADsticas_base_de_campeones',
	'lolnews': 'https://www.leagueoflegends.com/es-es/news/',
	'lolnotas': 'https://www.leagueoflegends.com/es-es/news/tags/patch-notes/',
}


class ScraperLOL:

	@classmethod
	def scraper(cls):
		champions = LOLChampionsPage.scrap(html_data = ReadFromWeb.read(URLS['lolchampions']))
		estadisticas = LOLFandomPage.scrap(html_data = ReadFromWeb.read(URLS['lolfandom']))
		noticias = LOLNewsNotesPage.scrap(html_data = ReadFromWeb.read(URLS['lolnews']))
		notas = LOLNewsNotesPage.scrap(html_data = ReadFromWeb.read(URLS['lolnotas']))

		return {
			'champions': champions,
			'estadisticas': estadisticas,
			'noticias': noticias,
			'notas': notas
		}

def main():
	ScraperLOL.scraper()

if __name__ == '__main__':
	main()