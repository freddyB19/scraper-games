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
	def decrypt(cls):
		#html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'decrypt.html'))
		html_parsed = ReadFromFile.read(os.path.join(cls.PATH, 'decrypt_ia.html'))


		if html_parsed is not None:
			noticia_principal = html_parsed.find('article', class_ = 'h-full')

			img = noticia_principal.find('img').get('src')
			categoria = noticia_principal.css.select('a div[class*="text-cc-pink-2"] span')[0].string.strip()
			titulo = noticia_principal.css.select(
				'h3[class*="font-akzidenz-grotes"] > a[class*="linkbox__overlay"]'
			)[0].string.strip()
			url = noticia_principal.css.select(
				'h3[class*="font-akzidenz-grotes"] > a[class*="linkbox__overlay"]'
			)[0].get('href')
			descripcion = noticia_principal.css.select('p[class*="mt-1 gg-dark:text-neutral-100"]')[0].string.strip()
			fecha = noticia_principal.css.select('footer div[class="mt-2 md:mt-4"] time')[0].string.strip()


			print(f"[+] Imagen: {img}")
			print(f"[+] Categoria: {categoria}")
			print(f"[+] Titulo: {titulo}")
			print(f"[+] Url: {url}")
			print(f"[+] Descripcion: {descripcion}")
			print(f"[+] Fecha: {fecha}")


			for articulo in html_parsed.css.select('article[class="w-full"] article[class="linkbox flex space-x-3"]'):
				categoria = articulo.find('p', class_='text-cc-pink-2').string.strip()
				url = articulo.find('a', class_='linkbox__overlay').get('href')
				titulo = [
					articulo.find('span', class_="bitcoin:group-hover:bg-orange-400").string.strip()
					if articulo.find('span', class_="bitcoin:group-hover:bg-orange-400")
					else None
				][0]
				fecha =  articulo.css.select('time[class!="inline-flex items-center gap-x-1"]')[0].string.strip()
				meta = articulo.css.select('time[class*="inline-flex"] span')[0].string.strip()

				print(f"\t[--] Categoria: {categoria}")
				print(f"\t[--] Url: {url}")
				print(f"\t[--] Titulo: {titulo}")
				print(f"\t[--] Fecha : {fecha}")
				print(f"\t[--] Meta : {meta}")

				print("\n\n")

			for articulo in html_parsed.css.select('article[class*="max-w-[764px]"] > article'):
				fecha = articulo.css.select('h4')[0].string.strip()

				categoria = articulo.find('p', class_ = "text-cc-pink-2").string.strip()
				url = articulo.find('a', class_="linkbox__overlay").get('href')
				titulo = articulo.css.select('a[class="linkbox__overlay"] span[class="font-medium"]')[0].string.strip()
				descripcion = articulo.find('p', class_="gg-dark:text-neutral-100").string.strip()
				meta = articulo.css.select('footer p[class*="flex"] time > span')[0].string.strip()

				print(f"\t[---] Fecha : {fecha}")
				print(f"\t[---] Categoria : {categoria}")
				print(f"\t[---] Url : {url}")
				print(f"\t[---] Titulo : {titulo}")
				print(f"\t[---] Descripcion : {descripcion}")
				print(f"\t[---] Meta : {meta}")

				print("\n\n")


	@classmethod
	def scraper(cls):
		#cls.elnacional_tecnologia()
		cls.decrypt()


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
