from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup


HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class JuegoGratuitosEASport:
	@classmethod
	def scrap(cls, html_data: HTMLParsed | None = None) -> str | List[Dict[str, str]]:

		if html_data is None:
			return None

		container = html_data.find('ea-box-set', layout="3up")

		if not container:
			return None

		lista_juegos_gratiutios = []

		for post in container.css.select('ea-container[filter-key="All"] ea-game-box'):
			lista_juegos_gratiutios.append({
				'titulo': post.get('main-link-title'),
				'url': f"{'https://www.ea.com'}{post.get('main-link-url')}",
				'imagen': post.get('background-image'),
				'logo': post.get('logo-url')
			})

		return lista_juegos_gratiutios
