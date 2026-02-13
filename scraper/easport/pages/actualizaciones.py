
from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)


def get_description(description: Tag | None) -> str | None:
	if not isinstance(description, Tag):
		return None

	return description.get_text().strip().replace("\n", "")

def get_data_from_element(element: Tag, tag_name: str, tag_property: str) -> str:	
	tag = element.find(tag_name)
	
	return tag.get(tag_property) if tag else None


class ActualizacionesEASport:
	@classmethod
	def scrap(cls, html_data: HTMLParsed | None) -> list[dict[str, str | None]] | None:
		if not html_data:
			return None

		container = html_data.find('ea-subheading', attrs={
			"title-text":"Últimas actualizaciones" ,
		})

		if not container:
			return None

		container = container.parent

		actualizaciones = []
		for nota in container.find_all('ea-container', attrs={'slot': "container"}):
			imagen = get_data_from_element(
				element = nota,
				tag_name = "ea-tile", 
				tag_property = "media"
			)
			titulo = get_data_from_element(
				element = nota,
				tag_name = "ea-tile", 
				tag_property = "title-text"
			)
			informacion = get_data_from_element(
				element = nota,
				tag_name = "ea-tile", 
				tag_property = "tooltip"
			)
			fecha = get_data_from_element(
				element = nota,
				tag_name = "ea-tile", 
				tag_property = "eyebrow-secondary-text"
			)
			url = get_data_from_element(
				element = nota,
				tag_name = "ea-cta", 
				tag_property = "link-url"
			)
			detalle = get_description(nota.find("ea-tile-copy", attrs={"slot":"copy"}))
			
			actualizaciones.append({
				"imagen": imagen,
				"titulo": titulo,
				"informacion": informacion,
				"fecha": fecha,
				"detalle": detalle,
				"url": url
			})
			
		return actualizaciones
