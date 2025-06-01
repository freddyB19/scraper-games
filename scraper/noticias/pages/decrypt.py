from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup


HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

ResponseDecrypt = NewType("ResponseDecrypt", Dict[str, Dict[str, str | List[ Dict[str, str] ] ]])

class DecryptNoticias:

	@classmethod
	def scrap(cls, html_parsed: HTMLParsed | None = None, url_root: str = "") -> str | ResponseDecrypt:
		if html_parsed is None:
			return None
		
		noticia_principal = html_parsed.find('article', class_ = 'h-full')

		if noticia_principal is None:
			return None

		imagen = noticia_principal.find('img').get('src')
		categoria = noticia_principal.css.select('a div[class*="text-cc-pink-2"] span')[0].string.strip()
		titulo = noticia_principal.css.select(
			'h3[class*="font-akzidenz-grotes"] > a[class*="linkbox__overlay"]'
		)[0].string.strip()
		url = noticia_principal.css.select(
			'h3[class*="font-akzidenz-grotes"] > a[class*="linkbox__overlay"]'
		)[0].get('href')
		descripcion = noticia_principal.css.select('p[class*="mt-1 gg-dark:text-neutral-100"]')[0].string.strip()
		fecha = noticia_principal.css.select('footer div[class="mt-2 md:mt-4"] time')[0].string.strip()

		noticias = {
			'principal': {
				'titulo': titulo,
				'url': f"{url_root}{url}",
				'categoria': categoria,
				'imagen': imagen,
				'descripcion': descripcion,
				'fecha': fecha,

			}
		}

		
		notas_cortas = []
		
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

			notas_cortas.append({
				'titulo': titulo,
				'url': f"{url_root}{url}",
				'categoria': categoria,
				'fecha': fecha,
				'meta': meta,
			})

		
		notas_extensas = []
		
		for articulo in html_parsed.css.select('article[class*="max-w-[764px]"] > article'):
			fecha = articulo.css.select('h4')[0].string.strip()

			categoria = articulo.find('p', class_ = "text-cc-pink-2").string.strip()
			url = articulo.find('a', class_="linkbox__overlay").get('href')
			titulo = articulo.css.select('a[class="linkbox__overlay"] span[class="font-medium"]')[0].string.strip()
			descripcion = articulo.find('p', class_="gg-dark:text-neutral-100").string.strip()
			meta = articulo.css.select('footer p[class*="flex"] time > span')[0].string.strip()

			notas_extensas.append({
				'titulo': titulo,
				'url': f"{url_root}{url}",
				'categoria': categoria,
				'fecha': fecha,
				'meta': meta,
				'descripcion': descripcion,
			})



		noticias['notas'] = {
			'cortas': notas_cortas,
			'extensas': notas_extensas
		}

		return noticias