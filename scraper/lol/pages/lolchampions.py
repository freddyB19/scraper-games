from typing import List
from typing import Dict
from typing import NewType

from collections import defaultdict

from bs4 import BeautifulSoup

HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class LOLChampionsPage:
	@classmethod
	def scrap(cls, html_data:HTMLParsed | None = None, champions_imagen:dict = {}, url_root: str = "") -> str | List[Dict[str, str]]:

		players = defaultdict(lambda: 'null', champions_imagen)

		if html_data is None:
			return None

		container = html_data.find('div', attrs={"data-testid": "card-grid"})
		
		champions = []

		if not container:
			return None

		for card in container.find_all('a'):

			url = card.get('href')
			champion = card.find('div', attrs={"data-testid": "card-title"}).string.strip()
			imagen = players[champion]

			champions.append({
				'url': f"{url_root}{url}",
				'imagen': imagen,
				'champion': champion
			})
		
		return champions

