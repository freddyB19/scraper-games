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
				'url': f"{'https://www.ea.com'}{novedad.get('main-link-url')}",
				'url-logo': novedad.get('logo-url')
			})


		if juegos_destacados:
			for juego in juegos_destacados:
				print(juego['img'])
				print(juego['titulo'])
				print(juego['url'])
				print()


	@classmethod
	def proximamente(cls):
		data = ReadFromFile.read(os.path.join(cls.PATH, 'proximamente.html'))
		
		html_parsed = BeautifulSoup(data, 'lxml')

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

 
		for prox_juego in lista_proximamente:
			print(prox_juego)
			print("\n\n")

	@classmethod
	def gratuitos(cls):
		data = ReadFromFile.read(os.path.join(cls.PATH, 'gratuitos.html'))
		html_parsed = BeautifulSoup(data, 'lxml')

		container = html_parsed.find('ea-box-set', layout="3up")
		for post in container.css.select('ea-container[filter-key="All"] ea-game-box'):
			print(post.get('main-link-title'))
			print(f"{'https://www.ea.com'}{post.get('main-link-url')}")
			print(post.get('background-image'))
			print(post.get('logo-url'))
			print()


	@classmethod
	def actualizaciones(cls):
		data = ReadFromFile.read(os.path.join(cls.PATH, 'easport.html'))
		html_parsed = BeautifulSoup(data, 'lxml')

		container = html_parsed.find('template')

		tabs = container.find_all('ea-tab')
		post_atc = container.find_all('ea-section', attrs={'spacing-top': "medium"})

		lista_actualizaciones= []
		for post_tag, post_info in zip(tabs, post_atc):
			#print(post_tag.string.strip())

			data = []
			for nota in  post_info.find_all('ea-container', slot="container"):
				data.append({
					'titulo': nota.find('h3').string.strip() if nota.find('h3') else 'null',
					'informacioón': [info.string.strip() for info in nota.find_all('div')],
					'detalle': nota.find('ea-tile-copy', slot='copy').string.strip(),
					'url': nota.find('ea-tile-copy', slot='copy').string.strip(),
					'imagen': nota.find('ea-tile').get('media')
				})

			lista_actualizaciones.append({
				post_tag.string.strip(): data
			})
			
		if lista_actualizaciones:
			for act in lista_actualizaciones:
				print(act)

	@classmethod
	def scraper(cls):
		#cls.noticias()
		#cls.novedades()
		#cls.proximamente()
		#cls.gratuitos()
		cls.actualizaciones()

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