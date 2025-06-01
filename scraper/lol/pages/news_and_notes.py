from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup

HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class LOLNewsNotesPage:

	@classmethod
	def scrap(cls, html_data:HTMLParsed | None = None, url_root: str = "") -> str | List[Dict[str, str]]:

		if html_data is None:
			return None
		
		container = html_data.css.select("section[id='news'] > div[data-testid='blade-content'] a")

		if not container:
			return None

		lista_info = []

		for info in container:
			
			categoria = info.find('div', attrs={"data-testid": "card-category"})
			
			lista_info.append({
				"titulo": info.get("aria-label"),
				"url": f"{url_root}{info.get('href')}" if url_root else info.get('href'),
				"imagen": info.find('img', attrs={"data-testid": "mediaImage"}).get("src"),
				"categoria": categoria.string.strip() if categoria is not None else None,
				"fecha": info.css.select('div > time')[0].get('datetime'),
				"detalle": info.css.select('div[data-testid="rich-text-html"] > div')[0].string.strip()
			})

		return lista_info
