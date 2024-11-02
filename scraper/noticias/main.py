import os
import sys

import httpx
from lxml import html
from bs4 import BeautifulSoup

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils.main import ReadFromWeb
from utils.main import ReadFromFile

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
	def elnacional(cls):
		#html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'elnacional_tecnologia.html'))

		html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'elnacional_ia.html'))

		if html_parsed is not None:
			contenido_principal = html_parsed.find('div', class_ = 'module-category')
			url =  contenido_principal.a.get('href')
			titulo =  contenido_principal.a.get('title')
			categoria = contenido_principal.find('div', class_='category').string.strip()
			fecha = contenido_principal.find('time').string.strip()
			no, protocolo, ruta = contenido_principal.find('div', class_='background-image').get('style').partition("https://")
			imagen = protocolo + ruta

			print(" +--- Noticia Principal ---+")
			print(f"[+] Url : {url}")
			print(f"[+] Titulo : {titulo}")
			print(f"[+] Categoria : {categoria}")
			print(f"[+] Fecha : {fecha}")
			print(f"[+] Imagen : {imagen}")
			print(" +--- --------------- ---+")

			for articulo in html_parsed.find_all('div', class_ = 'article'):
				imagen = articulo.css.select('div[class="image"] a img')[0].get("src")
				url = articulo.css.select('div[class="image"] a')[0].get("href")
				titulo = articulo.css.select('div[class="title"] a h2')[0].string.strip()
				meta = articulo.css.select('div[class="meta"] a[class="category"]')[0].get('title')
				fecha = articulo.css.select('div[class="meta"] time')[0].string.strip()
				extra = articulo.css.select('div[class="extract"] a')[0].string.strip()

				print(f"...[-] Imagen: {imagen}")
				print(f"...[-] Url: {url}")
				print(f"...[-] Titulo: {titulo}")
				print(f"...[-] Meta: {meta}")
				print(f"...[-] fecha: {fecha}")
				print(f"...[-] Extra: {extra}")

				print("-----------------")

				print()


		else:
			print(f"[-] Error: {html_parsed}")

	@classmethod
	def scraper(cls):
		cls.elnacional_tecnologia()

	@classmethod 
	def download(cls):
		
		for web in URL.keys():
			html_parsed = ReadFromWeb.read(url = URL[web])

			if html_parsed:
				with open(os.path.join(cls.PATH, f"{web}.html"), 'a') as file:
					file.write(html_parsed.prettify())
			else:
				print(f"[-] Error: {html_parsed}, Path: {web}")

def main():
	ScraperNoticias.scraper()

if __name__ == '__main__':
	main()
