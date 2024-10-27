import os
import sys
from typing import Dict

import httpx

from lxml import html

from bs4 import BeautifulSoup


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from utils.main import ReadFromFile
from utils.main import ReadFromWeb



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
	def novedades(cls):
		data = ReadFromFile.read(os.path.join(cls.PATH, 'novedades.html'))
		html_parsed = BeautifulSoup(data, 'lxml')

		container = html_parsed.find('ea-box-set')
		juegos_destacados = []
		
		for novedad in container.css.select('ea-container  ea-game-box[slot="game-box"]'):
			juegos_destacados.append({
				'img': novedad.get('background-image'),
				'titulo': novedad.get('main-link-title'),
				'url': f"{'https://www.ea.com'}{novedad.get('main-link-url')}"
			})


		if juegos_destacados:
			for juego in juegos_destacados:
				print(juego['img'])
				print(juego['titulo'])
				print(juego['url'])
				print()



	@classmethod
	def scraper(cls):
		#cls.noticias()
		cls.novedades()

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