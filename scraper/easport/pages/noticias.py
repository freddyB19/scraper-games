import re
from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)

def clean_title(title: str) -> str | None:
	if not isinstance(title, str):
		return None
	
	return title.strip()

def get_data_from_element(element: Tag) -> str | None:
	if not isinstance(element, Tag):
		return None

	return element.get_text().strip()

def get_tag(list_tag: list[Tag]) -> str | None:
	if not list_tag:
		return None
	return get_data_from_element(list_tag[0])

def get_date(list_date: list[Tag]) -> str | None:
	if not list_date:
		return None
	
	if not len(list_date) == 2:
		return None

	return get_data_from_element(list_date[1])

def get_description(description: Tag) -> str | None:
	if not isinstance(description, Tag):
		return None

	return description.get_text().strip()


class NoticiasEASport:
	@classmethod
	def scrap(cls, html_data: HTMLParsed | None = None) -> list[dict[str, str]] | None:
		if not html_data:
			return None

		container = html_data.find('ea-grid')

		if not container:
			return None

		lista_noticias = []

		for noticia in container.css.select('ea-container  ea-tile[slot="tile"]'):
			extra = noticia.find_all('div')

			lista_noticias.append({
				'imagen': noticia.get('media'),
				'titulo': clean_title(noticia.get('title-text')),
				'etiqueta': get_tag(extra),
				'fecha': get_date(extra),
				'descripcion': get_description(noticia.find('ea-tile-copy'))
			})

		return lista_noticias
