from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup


HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class ActualizacionesEASport:
	@classmethod
	def scrap(cls, html_data: HTMLParsed | None = None) -> str | List[Dict[str, str]]:
		if html_data is None:
			return None

		container = html_data.find('template')

		if not container:
			return None

		tabs = container.find_all('ea-tab')
		post_atc = container.find_all('ea-section', attrs={'spacing-top': "medium"})

		lista_actualizaciones = []
		
		etiquetas = []
		
		for post_tag, post_info in zip(tabs, post_atc):

			data = []
			for nota in  post_info.find_all('ea-container', slot="container"):
				data.append({
					'titulo': nota.find('h3').string.strip() if nota.find('h3') else 'null',
					'informacion': [info.string.strip() for info in nota.find_all('div')],
					'detalle': nota.find('ea-tile-copy', slot='copy').string.strip(),
					'url': nota.find('ea-cta', intent="news").get('link-url'),
					'imagen': nota.find('ea-tile').get('media')
				})

			etiquetas += [{'etiqueta': post_tag.string.strip(), 'info': data}]

		lista_actualizaciones.append({ 'etiqueta': etiquetas})
			
		return lista_actualizaciones
