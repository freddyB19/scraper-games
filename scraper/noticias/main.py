import os, sys, pprint

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)


from utils.main import ReadFromWeb, ReadFromFile, DownloadFile

from noticias.pages.marca import MarcaNoticias
from noticias.pages.lanacion import LaNacionNoticias


URL = {
	'lanacion': 'https://www.lanacion.com.ar/tema/videojuegos-tid48572/', 
	'lanacion_tecnologia': 'https://www.lanacion.com.ar/tecnologia/',
	'marca': 'https://www.marca.com/videojuegos/juegos.html?intcmp=MENUMIGA&s_kw=juegos',
}


class ScraperNoticias:

	@classmethod
	def scraper(cls) -> list[dict[str, list[dict[str, str]] | str]]:
		marca = MarcaNoticias.scrap( 
			html_parsed = ReadFromWeb.read(URL['marca'])
		)

		lanacion = LaNacionNoticias.scrap(
			html_parsed = ReadFromWeb.read(URL['lanacion']),
			url_root = 'https://www.lanacion.com.ar/'
		)
		lanacion_tecnologia = LaNacionNoticias.scrap(
			html_parsed = ReadFromWeb.read(URL['lanacion_tecnologia']),
			url_root = 'https://www.lanacion.com.ar/'
		)

		return [
			{'nombre': 'marca', 'pagina': marca},
			{
				'nombre': 'la nación', 
				'pagina': lanacion,
				'sub': {
					'nombre': 'la nación tecnología', 
					'pagina': lanacion_tecnologia
				}
			}
		]

def main():
	pprint.pprint(ScraperNoticias.scrap(), indent = 4)
	

if __name__ == '__main__':
	main()
