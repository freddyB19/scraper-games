from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup


HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)

def get_data_from_element(list_element: list[Tag]) -> str | None:
	if not list_element:
		return None

	if not isinstance(list_element[0], Tag):
		return None
	
	element = list_element[0]
	return element.get_text().strip()


class ProximamenteEASport:
	
	@classmethod
	def scrap(cls, html_data: HTMLParsed | None) -> list[dict[str, str | None]] | None:
		if not html_data:
			return None

		container = html_data.css.select('ea-section[layout="50:50"] ea-section-column[slot="section-column"]')

		if not container:
			return None

		lista_proximamente = []
		detail_game = lambda tag: {'url': tag.get('href'), 'tipo': tag.string.strip()}

		for post in container:
			tabla = post.find('ea-details-table', slot='details-table')

			if tabla:

				plataformas = list(
					map(
						detail_game, 
						tabla.css.select('ea-details-table-row:nth-of-type(2) div[text] a')
					)
				)
				
				generos = list(
					map(
						detail_game, 
						tabla.css.select('ea-details-table-row:nth-of-type(3) div[text] a')
					)
				)

				lista_proximamente.append({
					'titulo': get_data_from_element(post.css.select('ea-text[slot="text"] h5 b')), #[0].string.strip(),
					'fecha': get_data_from_element(tabla.css.select('ea-details-table-row:nth-of-type(1) div[text]')), #[0].string.strip(),
					'plataformas': plataformas,
					'genero': generos
				})

		
		return lista_proximamente