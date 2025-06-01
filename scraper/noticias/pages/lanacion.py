from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup


HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class LaNacionNoticias:

	@classmethod
	def scrap(cls, html_parsed: HTMLParsed | None = None, url_root: str = "") -> str | List[Dict[str, str]]:
		if html_parsed is None:
			return None

		articulos = html_parsed.find("div", class_="row-gap-tablet-3")

		if articulos is None:
			return None

		notas = []

		for articulo in articulos.find_all('article', class_="mod-article"):
			url = articulo.css.select('div[class="content-media"] a')[0].get('href')
			imagen = articulo.css.select('div[class="content-media"] img[class="com-image"]')[0].get('src')
			fecha = articulo.css.select('section[class="mod-description"] time')[0].string.strip()
			titulo = [
				articulo.css.select('h2[class*="com-title"] a[class="com-link"]')[0].string.strip()
				if articulo.css.select('h2[class*="com-title"] a[class="com-link"]')[0].string
				else [
					str(articulo.css.select('h2[class*="com-title"] a[class="com-link"]')[0].contents[0]), 
					articulo.css.select('h2[class*="com-title"] a[class="com-link"]')[0].contents[1]
				]
			][0]
			url_link = articulo.css.select('h2[class*="com-title"] a[class="com-link"]')[0].get("href")

			notas.append({
				'titulo': titulo,
				'url': f"{url_root}{url[1:]}",
				'imagen': imagen,
				'fecha': fecha,
				'url_link': url_link,
			})

		return notas