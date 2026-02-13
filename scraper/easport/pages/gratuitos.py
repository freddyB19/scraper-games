
from typing import TypeVar

from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)

class JuegoGratuitosEASport:
	@classmethod
	def scrap(cls, html_data: HTMLParsed | None, url_root: str) -> list[dict[str, str | None]] | None:

		if not html_data:
			return None

		container = html_data.find('ea-box-set', layout="3up")

		if not container:
			return None

		lista_juegos_gratiutios = []

		for post in container.css.select('ea-container[filter-key="All"] ea-game-box'):
			lista_juegos_gratiutios.append({
				'titulo': post.get('main-link-title'),
				'url': f"{url_root}{post.get('main-link-url')}",
				'imagen': post.get('background-image'),
				'logo': post.get('logo-url')
			})

		return lista_juegos_gratiutios
