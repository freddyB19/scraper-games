
from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)

def get_url(url: Tag, url_root: str = "") -> str:
	if not isinstance(url, Tag):
		return None

	return f"{url_root}{url.get('href')}" if url_root else url.get('href')

def get_category(category: Tag | None) -> str:
	if not isinstance(category, Tag):
		return None

	return category.get_text().strip()


def get_date(list_date: list[Tag]) -> str:
	if not list_date:
		return None

	if not isinstance(list_date[0], Tag):
		return None

	date = list_date[0]
	return date.get('datetime')

def get_detail(list_detail: list[Tag]) -> str:
	if not list_detail:
		return None

	if not isinstance(list_detail[0], Tag):
		return None

	detail = list_detail[0]
	return detail.get_text().strip()

class LOLNewsNotesPage:

	@classmethod
	def scrap(cls, html_data:HTMLParsed | None = None, url_root: str = "") -> str | list[dict[str, str]]:

		if html_data is None:
			return None
		
		container = html_data.css.select("section[id='news'] > div[data-testid='blade-content'] a")

		if not container:
			return None

		lista_info = []

		for info in container:
			lista_info.append({
				"titulo": info.get("aria-label"),
				"url": get_url(url = info, url_root = url_root),
				"categoria": get_category(info.find('div', attrs={"data-testid": "card-category"})), 
				"fecha": get_date(info.css.select('div > time')),
				"detalle": get_detail(info.css.select('div[data-testid="rich-text-html"] > div'))
			})
		
		return lista_info
