
class LOLChampionsPage:
	@classmethod
	def scrap(cls, html_data):

		if html_data is None:
			return "Error File"

		container = html_data.find('div', attrs={"data-testid": "card-grid"})
		
		champions = []

		if not container:
			return "Error"

		for card in container.find_all('a'):

			url = card.get('href')
			image = card.find('img').get('src')
			champion = card.find('div', attrs={"data-testid": "card-title"}).string

			champions.append({
				'url': url,
				'image': image,
				'champion': champion.strip()
			})
		
		return champions if champions else []

