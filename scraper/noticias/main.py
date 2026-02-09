import os, sys, pprint

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)


from utils.main import ReadFromWeb, ReadFromFile, DownloadFile

from noticias.pages.marca import MarcaNoticias
from noticias.pages.lanacion import LaNacionNoticias
from noticias.pages.wired import get_news, get_robots_news

URL = {
	'lanacion': 'https://www.lanacion.com.ar/tema/videojuegos-tid48572/', 
	'lanacion_tecnologia': 'https://www.lanacion.com.ar/tecnologia/',
	'marca': 'https://www.marca.com/videojuegos/juegos.html?intcmp=MENUMIGA&s_kw=juegos',
	'wired_espacio': 'https://es.wired.com/ciencia/espacio',
	'wired_biotecnologia': 'https://es.wired.com/ciencia/biotecnologia',
	'wired_neurociencia': 'https://es.wired.com/ciencia/neurociencia',
	'wired_robots': 'https://es.wired.com/tag/robots',
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

		wired_robots = get_robots_news(
			html_parsed = ReadFromWeb.read(URL["wired_robots"], url_root = URL["wired_robots"])
		)
		wired_neurociencia = get_news(
			html_parsed = ReadFromWeb.read(URL["wired_neurociencia"], url_root = URL["wired_neurociencia"])
			)
		wired_biotecnologia = get_news(
			html_parsed = ReadFromWeb.read(URL["wired_biotecnologia"], url_root = URL["wired_biotecnologia"])
		)
		wired_espacio = get_news(
			html_parsed = ReadFromWeb.read(URL["wired_espacio"], url_root = URL["wired_espacio"])
		)

		return [
			{'nombre': 'marca', 'pagina': marca},
			{
				'nombre': 'la nación', 
				'pagina': lanacion,
				'subs': [
					{
						'nombre': 'la nación tecnología', 
						'pagina': lanacion_tecnologia
					}
				]
			},
			{
				'nombre': 'wired',
				'subs': [
					{
						'nombre': 'wired robots',
						'pagina': wired_robots
					},
					{
						'nombre': 'wired neurociencia',
						'pagina': wired_neurociencia
					},
					{
						'nombre': 'wired biotecnologia',
						'pagina': wired_biotecnologia
					},
					{
						'nombre': 'wired spacio',
						'pagina': wired_espacio
					},

				]
			}
		]

def main():
	pprint.pprint(ScraperNoticias.scraper(), indent = 4)
	

if __name__ == '__main__':
	main()
