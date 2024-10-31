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
	@classmethod
	def scraper(cls):
		pass

	@classmethod 
	def download(cls):
		PATH = os.path.join(BASE, 'data', 'noticias')
		
		for web in URL.keys():
			html_parsed = ReadFromWeb.read(url = URL[web])

			if html_parsed:
				with open(os.path.join(PATH, f"{web}.html"), 'a') as file:
					file.write(html_parsed.prettify())
			else:
				print(f"[-] Error: {html_parsed}, Path: {web}")

def main():
	ScraperNoticias.download()

if __name__ == '__main__':
	main()

# git branch -c | -C albion noticias