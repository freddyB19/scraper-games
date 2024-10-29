import os
import sys
import json
from typing import Dict

import httpx

from lxml import html

from bs4 import BeautifulSoup



BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
from utils.main import ReadFromFile
from utils.main import ReadFromWeb

from easport.pages.noticias import NoticiasEASport
from easport.pages.novedades import NovedadesEASport
from easport.pages.gratuitos import JuegoGratuitosEASport
from easport.pages.proximamente import ProximamenteEASport



URL:Dict[str, str] = {
	'easport': 'https://www.ea.com/es-es',
	'noticias': 'https://www.ea.com/es-es/news',
	'novedades': 'https://www.ea.com/es-es/games',
	'proximamente' : 'https://www.ea.com/es-es/games/coming-soon',
	'gratuitos': 'https://www.ea.com/es-es/games/library/freetoplay'
}

class ScraperEASport:
	PATH = os.path.join(BASE, 'data', 'easport')

	@classmethod
	def noticias(cls):
		html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'noticias.html'))

		container = html_parsed.find('ea-grid')

		lista_noticias = []

		for noticia in container.css.select('ea-container  ea-tile[slot="tile"]'):
			extra = noticia.find_all('div')

			lista_noticias.append({
				'imagen': noticia.get('media'),
				'titulo': noticia.get('title-text'),
				'etiqueta': extra[0].string.strip(),
				'fecha': extra[1].string.strip(),
				'descripcion': noticia.find('ea-tile-copy').string.strip()
			})
		return lista_noticias
	
	@classmethod
	def novedades(cls):
		html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'novedades.html'))
	
		container = html_parsed.find('ea-box-set')
		
		juegos_destacados = []
		
		for novedad in container.css.select('ea-container  ea-game-box[slot="game-box"]'):
			juegos_destacados.append({
				'img': novedad.get('background-image'),
				'titulo': novedad.get('main-link-title'),
				'url': f"{'https://www.ea.com'}{novedad.get('main-link-url')}",
				'url-logo': novedad.get('logo-url')
			})


		return juegos_destacados


	@classmethod
	def proximamente(cls):
		html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'proximamente.html'))
		
		container = html_parsed.css.select('ea-section[layout="50:50"] ea-section-column[slot="section-column"]')

		lista_proximamente = []

		for post in container:
			tabla = post.find('ea-details-table', slot='details-table')

			if tabla:

				plataformas = list(
					map(
						lambda tag: {'url': tag.get('href'), 'tipo': tag.string.strip()}, 
						tabla.css.select('ea-details-table-row:nth-of-type(2) div[text] a')
					)
				)
				
				generos = list(
					map(
						lambda tag: {'url': tag.get('href'), 'genero': tag.string.strip()}, 
						tabla.css.select('ea-details-table-row:nth-of-type(3) div[text] a')
					)
				)

				lista_proximamente.append({
					'titulo': post.css.select('ea-text[slot="text"] h5 b')[0].string.strip(),
					'fecha': tabla.css.select('ea-details-table-row:nth-of-type(1) div[text]')[0].string.strip(),
					'plataformas': plataformas,
					'genero': generos
				})

		
		return lista_proximamente
		
	@classmethod
	def gratuitos(cls):
		html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'gratuitos.html'))

		container = html_parsed.find('ea-box-set', layout="3up")

		lista_juegos_gratiutios = []

		for post in container.css.select('ea-container[filter-key="All"] ea-game-box'):
			lista_juegos_gratiutios.append({
				'titulo': post.get('main-link-title'),
				'url': f"{'https://www.ea.com'}{post.get('main-link-url')}",
				'imagen': post.get('background-image'),
				'logo': post.get('logo-url')
			})

		return lista_juegos_gratiutios


	@classmethod
	def actualizaciones(cls):
		html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'easport.html'))

		container = html_parsed.find('template')

		tabs = container.find_all('ea-tab')
		post_atc = container.find_all('ea-section', attrs={'spacing-top': "medium"})

		lista_actualizaciones = []
		etiquetas = []
		for post_tag, post_info in zip(tabs, post_atc):

			data = []
			for nota in  post_info.find_all('ea-container', slot="container"):
				data.append({
					'titulo': nota.find('h3').string.strip() if nota.find('h3') else 'null',
					'información': [info.string.strip() for info in nota.find_all('div')],
					'detalle': nota.find('ea-tile-copy', slot='copy').string.strip(),
					'url': nota.find('ea-tile-copy', slot='copy').string.strip(),
					'imagen': nota.find('ea-tile').get('media')
				})

			etiquetas += [{'etiqueta': post_tag.string.strip(), 'info': data}]

		lista_actualizaciones.append({ 'etiqueta': etiquetas})
			
		return lista_actualizaciones


	@classmethod
	def scraper(cls):
		#noticias = cls.noticias()
		noticias = NoticiasEASport.scrap(
			html_data = ReadFromFile.read(os.path.join(BASE, 'data', 'easport', 'easport.html'))
		)	
		#novedades = cls.novedades()
		novedades = NovedadesEASport.scrap(
			html_data = ReadFromFile.read(os.path.join(BASE, 'data', 'easport', 'novedades.html'))
		)

		#proximamente = cls.proximamente()
		proximamente = ProximamenteEASport.scrap(
			html_data = ReadFromFile.read(os.path.join(BASE, 'data', 'easport', 'proximamente.html'))
		)
		
		#gratuitos = cls.gratuitos()
		gratuitos = JuegoGratuitosEASport.scrap(
			html_data = ReadFromFile.read(os.path.join(BASE, 'data', 'easport', 'gratuitos.html'))
		)

		
		actualizaciones = cls.actualizaciones()

		easport = {
			'noticias': noticias,
			'novedades': novedades,
			'proximamente': proximamente,
			'gratuitos': gratuitos,
			'actualizaciones': actualizaciones,

		}

		print(easport['gratuitos'])

		"""
		with open(os.path.join(BASE, 'results', 'easport.json'), 'a') as file:
			json.dump(easport, file, indent=4)
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