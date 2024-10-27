import os
import sys
from typing import Dict

import httpx

from lxml import html

from bs4 import BeautifulSoup


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from utils.main import ReadFromFile

URL:Dict[str, str] = {
	'easport': 'https://www.ea.com/es-es',
	'noticias': 'https://www.ea.com/es-es/news',
	'novedades': 'https://www.ea.com/es-es/games',
	'proximamente' : 'https://www.ea.com/es-es/games/coming-soon',
	'ofertas': 'https://www.ea.com/es-es/sales/deals',
	'gratuitos': 'https://www.ea.com/es-es/games/library/freetoplay'
}

class ScraperEASport:
	PATH = os.path.join(BASE, 'data', 'easport')

	@classmethod
	def noticias(cls):
		data = ReadFromFile.read(os.path.join(cls.PATH, 'noticias.html'))
		html_parsed = BeautifulSoup(data, 'lxml')

		container = html_parsed.find('ea-grid')

		for noticia in container.css.select('ea-container  ea-tile[slot="tile"]'):
			print(f"Imagen: {noticia.get('media')}")
			print(f"Titulo: {noticia.get('title-text')}")
			extra = noticia.find_all('div')
			print(f"Tag: {extra[0].string.strip()} -- Fecha: {extra[1].string.strip()}")
			print(f"Descripcion: {noticia.find('ea-tile-copy').string.strip()}")
			print()
	

	@classmethod
	def scraper(cls):
		cls.noticias()

		"""
		path = os.path.join(BASE, 'data', 'easport', 'easport.html')
		data = ReadFromFile.read(path)

		html_parsed = BeautifulSoup(data, 'lxml')

		container = html_parsed.find('ea-box-set', unresolved=True, attrs={'spacing-top': 'none'})

		print("Juegos destacados")
		for destacados in container.find_all('ea-container', slot='container'):
			juego = destacados.find('ea-game-box')
			print(juego.get('main-link-title'))
			print(juego.get('background-image'))
			print(f"{'https://www.ea.com'}{juego.get('main-link-url')}")
			print()
		"""

	@classmethod
	def download(cls):
		response = httpx.get(URL['gratuitos'])
		
		if response.status_code == 200:
			page = html.fromstring(response.text)
			html_parsed = BeautifulSoup(html.tostring(page), 'lxml')

			with open(os.path.join(BASE, 'data', 'easport', 'gratuitos.html'), 'a') as file:
				file.write(html_parsed.prettify())


def main():
	ScraperEASport.scraper()


if __name__ == '__main__':
	main()