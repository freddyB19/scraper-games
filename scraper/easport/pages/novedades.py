
from typing import TypeVar

from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)

class NovedadesEASport:

	@classmethod
	def scrap(cls, html_data: HTMLParsed | None, url_root: str) -> list[dict[str, str | None]] | None:
		if not html_data:
			return None

		container = html_data.find('ea-box-set')
		
		if not container:
			return None

		juegos_destacados = []
		
		for novedad in container.css.select('ea-container  ea-game-box[slot="game-box"]'):
			juegos_destacados.append({
				'imagen': novedad.get('background-image'),
				'titulo': novedad.get('main-link-title'),
				'url': f"{url_root}{novedad.get('main-link-url')}",
				'logo': novedad.get('logo-url')
			})


		return juegos_destacados

