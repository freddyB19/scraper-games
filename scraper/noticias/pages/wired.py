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
			articulo.css.select('a[class*="SummaryItemHedLink-cxRzVg"] h3[class*="SummaryItemHedBase-hnYOxl"]')
		)
		summary = get_text_from_element(
			articulo.css.select('div[class*="BaseText-eqOrNE"]')
		)
		image = get_data_from_element(
			articulo.css.select('picture[class*="ResponsiveImagePicture-cGZhnX"] img[class*="ResponsiveImageContainer-eNxvmU"]'), 
			tag_property = "src"
		)
		url = get_data_from_element(
			articulo.css.select('a[class*="SummaryItemHedLink-cxRzVg"]'), 
			tag_property = "href"
		)
		
		notas.append({
			"title": title,
			"image": image,
			"summary": summary,
			"url": f"{url_root}{url}"
		})
	return notas

def get_robots_news(html_parsed: HTMLParsed, url_root:str = "") -> list[dict[str, str]]:
	if not html_parsed:
		return None

	content = html_parsed.find("div", class_="GridItem-beYvyV iEWjAa grid--item grid-layout__content")

	return extrac_news(
		list_news = content.css.select('div[class="summary-list__items"] div[class*="SummaryItemWrapper-ircdWR"]'),
		url_root = url_root
	)

def get_news(html_parsed: HTMLParsed, url_root: str = "") -> list[dict[str, str]]:
	if not html_parsed:
		return None
	
	content_sections = html_parsed.find("div", class_="SummaryRiverWrapper-cA-dhEp KKSYe")

	if not content_sections:
		return None

	sections = content_sections.css.select('section[class*="SummaryRiverSection-kUGpHj"] ')
	articulos = [
		articulo
		for section in sections
		for articulo in section.css.select('div[class="summary-list__items"] div[class*="SummaryItemWrapper-ircdWR"]')
	]

	return extrac_news(list_news = articulos, url_root = url_root)
