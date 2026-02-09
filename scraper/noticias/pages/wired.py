import pprint

from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound = BeautifulSoup)


def extrac_news(list_news: list[Tag], url_root: str = "") -> list[dict[str, str]]:
	notas = []
	for articulo in list_news:
		titulo =  articulo.css.select('a[class*="SummaryItemHedLink-cxRzVg"] h3[class*="SummaryItemHedBase-hnYOxl"]')[0].get_text().strip().replace("\n", "")
		imagen = articulo.css.select('picture[class*="ResponsiveImagePicture-cGZhnX"] img[class*="ResponsiveImageContainer-eNxvmU"]')[0].get("src")
		resum = articulo.css.select('div[class*="BaseText-eqOrNE"]')[0].get_text().strip().replace("\n", "")
		url = articulo.css.select('a[class*="SummaryItemHedLink-cxRzVg"]')[0].get("href")
		
		notas.append({
			"titulo": titulo,
			"imagen": imagen,
			"resum": resum,
			"url": f"{url_root}{url[1:]}"
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

def get_news(html_parsed: HTMLParsed) -> list[dict[str, str]]:
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
