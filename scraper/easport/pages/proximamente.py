from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup


HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class ProximamenteEASport:
	
	@classmethod
	def scrap(cls, html_data: HTMLParsed | None = None) -> str | List[Dict[str, str]]:
		if html_data is None:
			return None

		container = html_data.css.select('ea-section[layout="50:50"] ea-section-column[slot="section-column"]')

		if not container:
			return None

		lista_proximamente = []

		for post in container:
			tabla = post.find('ea-details-table', slot='details-table')

			if tabla:

				plataformas = list(
					map(
						lambda tag: {'url': tag.get('href'), 'tipo': tag.string.strip()}, 
						tabla.css.select('ea-details-table-row:nth-of-type(2) div[text] a')
					)
				)
				
				generos = list(
					map(
						lambda tag: {'url': tag.get('href'), 'genero': tag.string.strip()}, 
						tabla.css.select('ea-details-table-row:nth-of-type(3) div[text] a')
					)
				)

				lista_proximamente.append({
					'titulo': post.css.select('ea-text[slot="text"] h5 b')[0].string.strip(),
					'fecha': tabla.css.select('ea-details-table-row:nth-of-type(1) div[text]')[0].string.strip(),
					'plataformas': plataformas,
					'genero': generos
				})

		
		return lista_proximamente