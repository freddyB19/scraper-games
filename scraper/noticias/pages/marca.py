from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup


HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class MarcaNoticias:

	@classmethod
	def scrap(cls, html_parsed: HTMLParsed | None = None) -> str | List[Dict[str, str]]:

		if html_parsed is None:
			return None

		articulos = html_parsed.find('div', class_="ue-l-cover-grid__column size8of12")


		if articulos is None:
			return None

		notas = []
		for articulo in articulos.css.select('div[class*="ue-l-cover-grid__unit"] article[class*="ue-c-cover-content"]'):
			imagen = articulo.find('img').get('src')
			meta = articulo.find('span', class_="ue-c-cover-content__kicker").string.strip()
			url = articulo.find('a', class_="ue-c-cover-content__link").get('href')
			titulo = articulo.find('h2', class_="ue-c-cover-content__headline").string.strip()
			autor = articulo.find('span', class_='hidden-content').next_sibling.strip()

			notas.append({
				'titulo': titulo,
				'url': url,
				'imagen': imagen,
				'meta': meta,
				'autor': autor,
			})

		return notas