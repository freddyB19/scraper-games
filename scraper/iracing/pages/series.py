import pprint
from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup


HTMLParsed = TypeVar("HTMLParsed", bound = BeautifulSoup)


def get_data_from_element(list_tag: list[Tag], tag_property: str) -> str:
	if not list_tag:
		return None
	if not isinstance(list_tag[0], Tag):
		return None

	element = list_tag[0]
	return element.get(tag_property)

def get_name_serie(list_tag: list[Tag]) -> str:
	if not list_tag:
		return None
	if not isinstance(list_tag[0], Tag):
		return None

	name = list_tag[0]
	return name.get_text().strip()

def get_type_serie(type: Tag | None) -> str:
	if not isinstance(type, Tag):
		return None

	return type.get_text().strip()


def get_series(html: HTMLParsed | None):
	if not html:
		return None

	container = html.find("div", id="page")

	if not container:
		return None

	series = []
	for serie in container.css.select("div[class='clearfix']:not(div[id])"):
		type = get_type_serie(serie.find("h2"))

		list_series = [	
			{
				"url": get_data_from_element(
					type.css.select('div[class="grid-item-content-container"] a'),
					tag_property = "href"
				),
				"image": get_data_from_element(
					type.css.select('div[class="grid-item-content-container"] a img'),
					tag_property = "src"
				),
				"name": get_name_serie(
					type.css.select('div[class="grid-item-content"] span  a')
				)
			}
			
			for type in serie.css.select("div[class='clearfix']:not(div[id]) > div")
		]
		
		series.append({
			"name": type,
			"data": list_series
		})
	
	return series
