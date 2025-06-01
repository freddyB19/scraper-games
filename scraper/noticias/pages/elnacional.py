from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup


HTMLParsed = NewType("HTMLParsed", BeautifulSoup)
ResponseElNacional = NewType("ResponseElNacional", Dict[str, Dict[str, str | List[ Dict[str, str] ] ]])


class ElNacionalNoticias:

	@classmethod
	def scrap(cls, html_parsed: HTMLParsed | None = None, url_root: str = "") -> str | ResponseElNacional:
		
		if html_parsed is None:
			return None

		contenido_principal = html_parsed.find('div', class_ = 'module-category')
		
		if contenido_principal is None:
			return None

		url =  contenido_principal.a.get('href')
		titulo =  contenido_principal.a.get('title')
		categoria = contenido_principal.find('div', class_='category').string.strip()
		fecha = contenido_principal.find('time').string.strip()
		no, protocolo, ruta = contenido_principal.find('div', class_='background-image').get('style').partition("https://")
		imagen = protocolo + ruta

		noticias = {
			'principal': {
				'titulo': titulo,
				'url': url,
				'categoria': categoria,
				'fecha': fecha,
				'imagen': imagen,
			}
		}

		notas = []
		
		for articulo in html_parsed.find_all('div', class_ = 'article'):
			imagen = articulo.css.select('div[class="image"] a img')[0].get("src")
			url = articulo.css.select('div[class="image"] a')[0].get("href")
			titulo = articulo.css.select('div[class="title"] a h2')[0].string.strip()
			meta = articulo.css.select('div[class="meta"] a[class="category"]')[0].get('title')
			fecha = articulo.css.select('div[class="meta"] time')[0].string.strip()
			extra = articulo.css.select('div[class="extract"] a')[0].string.strip()

			notas.append({
				'titulo': titulo,
				'url': url,
				'imagen': imagen,
				'meta': meta,
				'fecha': fecha,
				'extra': extra,
			})


		noticias['notas'] = notas

		return noticias