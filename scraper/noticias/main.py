import os
import sys
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils.main import ReadFromWeb
from utils.main import ReadFromFile

from pages.marca import MarcaNoticias
from pages.decrypt import DecryptNoticias
from pages.lanacion import LaNacionNoticias
from pages.elnacional import ElNacionalNoticias


URL = {
	'elnacional_tecnologia': 'https://www.elnacional.com/tecnologia/' ,
	'elnacional_ia': 'https://www.elnacional.com/inteligencia-artificial/?utm_source=menu&utm_medium=recirculation&utm_campaign=internal_links',
	'lanacion': 'https://www.lanacion.com.ar/tema/videojuegos-tid48572/', 
	'marca': 'https://www.marca.com/videojuegos/juegos.html?intcmp=MENUMIGA&s_kw=juegos',
	'decrypt': 'https://decrypt.co/es/news/technology',
	'decrypt_ia': 'https://decrypt.co/es/news/artificial-intelligence'
}


class ScraperNoticias:
	PATH = os.path.join(BASE, 'data', 'noticias')
	
	@classmethod
	def scraper(cls):

		marca = MarcaNoticias.scrap( 
			html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'marca.html'))
		)
		
		lanacion = LaNacionNoticias.scrap(
			html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'lanacion.html')), 
			url_root = URL['lanacion']
		)

		decrypt_tecnologia = DecryptNoticias.scrap(
			html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'decrypt.html')),
			url_root = URL['decrypt']
		)

		decrypt_ia = DecryptNoticias.scrap(
			html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'decrypt_ia.html')),
			url_root = URL['decrypt_ia']
		)

		elnacional_tecnologia = ElNacionalNoticias.scrap(
			html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'elnacional_tecnologia.html')),
			url_root = URL['elnacional_tecnologia']
		)
		
		elnacional_ia = ElNacionalNoticias.scrap(
			html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'elnacional_ia.html')),
			url_root = URL['elnacional_ia']
		)

		noticias = {
			'marca': marca,
			'lanacion': lanacion,
			'decrypt_tecnologia': decrypt_tecnologia,
			'decrypt_ia': decrypt_ia,
			'elnacional_tecnologia': elnacional_tecnologia,
			'elnacional_ia': elnacional_ia,

		}

		with open(os.path.join(cls.PATH, 'noticias.json'), 'a') as archivo:
				json.dump(noticias, archivo, indent=4)

def main():
	ScraperNoticias.scraper()

if __name__ == '__main__':
	main()
