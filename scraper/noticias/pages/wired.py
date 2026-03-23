import pprint

from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound = BeautifulSoup)


def get_data_from_element(list_tag: list[Tag], tag_property: str) -> str | None:
	if not list_tag:
		return None

	if not isinstance(list_tag[0], Tag):
		return None

	element = list_tag[0]

	return element.get(tag_property)

def get_text_from_element(list_tag: list[Tag]):
	if not list_tag:
		return None

	if not isinstance(list_tag[0], Tag):
		return None

	element = list_tag[0]
	return element.get_text().strip().replace("\n", "").replace("  ", "")


def extrac_news(list_news: list[Tag], url_root: str = "") -> list[dict[str, str]]:
	notas = []

	for articulo in list_news:
		title =  get_text_from_element(
			articulo.css.select('a[class*="summary-item-tracking__hed-link"] h3[class*="summary-item__hed"]')
		)
		summary = get_text_from_element(
			articulo.css.select('div[class*="summary-item__dek"]')
		)
		image = get_data_from_element(
			articulo.css.select('picture[class*="summary-item__image"] img[class*="responsive-image__image"]'), 
			tag_property = "src"
		)
		url = get_data_from_element(
			articulo.css.select('a[class*="summary-item-tracking__hed-link"]'), 
			tag_property = "href"
		)

		notas.append({
			"title": title,
			"image": image,
			"summary": summary,
			"url": f"{url_root}{url}"
		})

	notas_filter = [nota for nota in notas if not None in nota.values()] 
	return notas_filter

def get_robots_news(html_parsed: HTMLParsed, url_root:str = "") -> list[dict[str, str]]:
	if not html_parsed:
		return None

	content = html_parsed.find("section", attrs={"data-testid": "SummaryRiverSection"})

	if not content:
		return None

	return extrac_news(
		list_news = content.css.select('div[class="summary-list__items"] div[class*="summary-item"]'),
		url_root = url_root
	)

def get_news(html_parsed: HTMLParsed, url_root: str = "") -> list[dict[str, str]]:
	if not html_parsed:
		return None
	
	content_sections = html_parsed.find("div", attrs={"data-testid":"SummaryRiverWrapper"})

	if not content_sections:
		return None

	sections = content_sections.css.select('section[data-testid*="SummaryRiverSection"] ')
	articulos = [
		articulo
		for section in sections
		for articulo in section.css.select('div[class="summary-list__items"] div[class*="summary-item"]')
	]

	return extrac_news(list_news = articulos, url_root = url_root)
