import pprint

from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup


HTMLParsed = TypeVar("HTMLParsed", bound = BeautifulSoup)


def get_url(list_url: list[Tag]) -> str | None:
	if not list_url:
		return None
	
	if not isinstance(list_url[0], Tag):
		return None
	
	url = list_url[0]
	return url.get('href')


def clean_title(title: str) -> str:
	return title.strip().replace("\n", "").replace("  ", "")

def get_title(list_title: list[Tag]) -> str | None:
	if not list_title:
		return None
	if not isinstance(list_title[0], Tag):
		return None

	title = list_title[0]
	return clean_title(title.get_text())


def get_url_image(list_img: list[Tag]) -> str | None:
	if not list_img:
		return None
	if not isinstance(list_img[0], Tag):
		return None

	img = list_img[0]
	return img.get('src')


def clean_date(time: str) -> str:
	return time.strip().replace("\n", "")

def get_date(list_time: list[Tag]) -> str | None:
	if not list_time:
		return None
	if not isinstance(list_time[0], Tag):
		return None

	time = list_time[0]
	return clean_date(time.get_text())


class LaNacionNoticias:

	@classmethod
	def scrap(cls, html_parsed: HTMLParsed | None = None, url_root: str = "") -> None | list[dict[str, str]]:
		if html_parsed is None:
			return None

		articulos = html_parsed.find("div", class_="row-gap-tablet-3")

		if articulos is None:
			return None

		notas = []
		for articulo in articulos.find_all('article', class_="mod-article"):
			url = get_url(articulo.css.select('div[class="content-media"] a'))
			imagen = get_url_image(articulo.css.select('div[class="content-media"] img[class*="image"]'))
			fecha = get_date(articulo.css.select('section[class="mod-description"] time'))
			
			titulo = get_title(
				articulo.css.select('h2[class*="com-title"] a[class="com-link"]')
			)

			notas.append({
				'titulo': titulo,
				'url': f"{url_root}{url[1:]}",
				'url_link': url,
				'imagen': imagen,
				'fecha': fecha
			})

		return notas
