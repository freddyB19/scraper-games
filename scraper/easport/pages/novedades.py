from typing import List
from typing import Dict
from typing import NewType


from bs4 import BeautifulSoup

HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class NovedadesEASport:

	@classmethod
	def scrap(cls, html_data: HTMLParsed | None = None) -> str | List[Dict[str, str]]:
		if html_data is None:
			return None

		container = html_data.find('ea-box-set')
		
		if not container:
			return None

		juegos_destacados = []
		
		for novedad in container.css.select('ea-container  ea-game-box[slot="game-box"]'):
			juegos_destacados.append({
				'imagen': novedad.get('background-image'),
				'titulo': novedad.get('main-link-title'),
				'url': f"{'https://www.ea.com'}{novedad.get('main-link-url')}",
				'logo': novedad.get('logo-url')
			})


		return juegos_destacados

