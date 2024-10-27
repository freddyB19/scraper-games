import os

from typing import Dict

import httpx

from lxml import html

from bs4 import BeautifulSoup

from utils.main import ReadFromFile

URL:Dict[str, str] = {
	'easport': 'https://www.ea.com/es-es',
	'noticias': 'https://www.ea.com/es-es/news',
	'novedades': 'https://www.ea.com/es-es/games',
	'proximamente' : 'https://www.ea.com/es-es/games/coming-soon',
	'ofertas': 'https://www.ea.com/es-es/sales/deals',
	'gratuitos': 'https://www.ea.com/es-es/games/library/freetoplay'
}

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class ScraperEASport:

	@classmethod
	def scraper(cls):
		path = os.path.join(BASE, 'data', 'easport', 'easport.html')
		data = ReadFromFile.read(path)

		html_parsed = BeautifulSoup(data, 'lxml')

		container = html_parsed.find('ea-box-set', unresolved=True, attrs={'spacing-top': 'none'})

		for destacados in container.find_all('ea-container', slot='container'):
			print(destacados['ea-game-box '].get('background-image'))



	@classmethod
	def download(cls):
		response = httpx.get(URL['easport'])
		
		if response.status_code == 200:
			page = html.fromstring(response.text)
			html_parsed = BeautifulSoup(html.tostring(page), 'lxml')

			with open(os.path.join(BASE, 'data', 'easport', 'easport.html'), 'a') as file:
				file.write(html_parsed.prettify())


def main():
	ScraperEASport.scraper()


if __name__ == '__main__':
	main()