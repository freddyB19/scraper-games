from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup

HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class LOLNewsNotesPage:

	@classmethod
	def scrap(cls, html_data:HTMLParsed | None = None) -> str | List[Dict[str, str]]:

		if html_data is None:
			return "Error File"
		
		container = html_data.find('div', class_ = "sc-1de19c4d-0 jhZjMa")

		if not container:
			return "Error []"

		lista_info = []
		
		for info in container.find_all('a'):
			
			categoria = info.find('div', attrs={"data-testid": "card-category"})
			
			lista_info.append({
				"titulo": info.get("aria-label"),
				"url": info.get("href"),
				"image": info.find('img', attrs={"data-testid": "mediaImage"}).get("src"),
				"categoria": categoria.string.strip() if categoria is not None else None,
				"fecha": info.css.select('div > time')[0].get('datetime'),
				"detalle": info.css.select('div[data-testid="rich-text-html"] > div')[0].string.strip()
			})

		return lista_info
