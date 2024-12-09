import os
import sys
from typing import Dict
from typing import List


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils.main import ReadFromWeb
from utils.main import ReadFromFile

from noticias.pages.marca import MarcaNoticias
from noticias.pages.decrypt import DecryptNoticias
from noticias.pages.lanacion import LaNacionNoticias
from noticias.pages.elnacional import ElNacionalNoticias


URL:Dict[str, str] = {
	'elnacional_tecnologia': 'https://www.elnacional.com/tecnologia/' ,
	'elnacional_ia': 'https://www.elnacional.com/inteligencia-artificial/',
	'lanacion': 'https://www.lanacion.com.ar/tema/videojuegos-tid48572/', 
	'marca': 'https://www.marca.com/videojuegos/juegos.html?intcmp=MENUMIGA&s_kw=juegos',
	'decrypt': 'https://decrypt.co/es/news/technology',
	'decrypt_ia': 'https://decrypt.co/es/news/artificial-intelligence'
}


class ScraperNoticias:

	@classmethod
	def scraper(cls) -> Dict[str, Dict | List[Dict]]:

		marca = MarcaNoticias.scrap( 
			html_parsed = ReadFromWeb.read(URL['marca'])
		)

		lanacion = LaNacionNoticias.scrap(
			html_parsed = ReadFromWeb.read(URL['lanacion']),
			url_root = 'https://www.lanacion.com.ar/'
		)
		
		decrypt_tecnologia = DecryptNoticias.scrap(
			html_parsed = ReadFromWeb.read(URL['decrypt']),
			url_root = 'https://decrypt.co'
		)

		decrypt_ia = DecryptNoticias.scrap(
			html_parsed = ReadFromWeb.read(URL['decrypt_ia']),
			url_root = 'https://decrypt.co'
		)

		elnacional_tecnologia = ElNacionalNoticias.scrap(
			html_parsed = ReadFromWeb.read(URL['elnacional_tecnologia']),
			url_root = URL['elnacional_tecnologia']
		)
		
		elnacional_ia = ElNacionalNoticias.scrap(
			html_parsed = ReadFromWeb.read(URL['elnacional_ia']),
			url_root = URL['elnacional_ia']
		)

		return [
			{'nombre': 'marca', 'pagina': marca},
			{'nombre': 'lanacion', 'pagina': lanacion},
			{'nombre': 'decrypt_tecnologia', 'pagina': decrypt_tecnologia},
			{'nombre': 'decrypt_ia', 'pagina': decrypt_ia},
			{'nombre': 'elnacional_tecnologia', 'pagina': elnacional_tecnologia},
			{'nombre': 'elnacional_ia', 'pagina': elnacional_ia}
		]

def main():
	ScraperNoticias.scraper()

if __name__ == '__main__':
	main()
