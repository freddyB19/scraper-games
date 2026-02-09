from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)


def get_img(img: Tag | None) -> str | None:
	return img.get('src') if isinstance(img, Tag) else None

def get_meta(meta: Tag | None) -> str | None:
	return meta.get_text().strip() if isinstance(meta, Tag) else None

def get_title(title: Tag | None) -> str | None:
	return title.get_text().strip() if isinstance(title, Tag) else None

def get_url(url: Tag | None) -> str | None:
	return url.get('href') if isinstance(url, Tag) else None

def get_author(author: Tag | None) -> str | None:
	if not isinstance(author, Tag):
		return None

	name = author.next_sibling
	return name.strip() if name else None

class MarcaNoticias:

	@classmethod
	def scrap(cls, html_parsed: HTMLParsed | None = None) -> str | list[dict[str, str]]:

		if not html_parsed:
			return None

		articulos = html_parsed.find('div', class_="ue-l-cover-grid__column size8of12")

		if not articulos:
			return None

		notas = []

		for articulo in articulos.css.select('div[class*="ue-l-cover-grid__unit"] article[class*="ue-c-cover-content"]'):			
			imagen = get_img(articulo.find('img'))
			meta = get_meta(articulo.find('span', class_="ue-c-cover-content__kicker"))
			url = get_url(articulo.find('a', class_="ue-c-cover-content__link"))
			titulo = get_title(articulo.find('h2', class_="ue-c-cover-content__headline"))
			autor = get_author(articulo.find('span', class_='hidden-content'))
			
			notas.append({
				'titulo': titulo,
				'url': url,
				'imagen': imagen,
				'meta': meta,
				'autor': autor,
			})


		return notas
