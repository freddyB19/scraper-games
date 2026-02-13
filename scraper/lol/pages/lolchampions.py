import pprint, asyncio, random
from typing import TypeVar
from dataclasses import dataclass

from bs4.element import Tag
from bs4 import BeautifulSoup

from utils.main import AsyncReadFromWeb, run_task

HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)

SEMAPHORE_LIMIT = 5
peticiones_sem = asyncio.Semaphore(SEMAPHORE_LIMIT)

@dataclass
class ChampionBase:
	url: str
	champion: str


def get_img_champions(html: HTMLParsed) -> list[str] | None:
	if not html:
		return None

	content = html.find("section", attrs={"data-testid": "landing-media-carousel"})

	if not content:
		return None

	images = []
	for img in content.css.select('div[class*="sc-cf6885cf-0"] img[class*="sc-de10a588-0"]', limit = 6):
		images.append(img.get("src"))

	return list(set(images)) if images else None


def get_champion(champion: Tag | None) -> str:
	return champion.get_text().strip() if isinstance(champion, Tag) else None


async def get_images(champion: ChampionBase) -> dict[str, str | list[str] | None]:
	async with peticiones_sem:
		content = await AsyncReadFromWeb.read(champion.url)
	
	images = await run_task(get_img_champions, content)

	await asyncio.sleep(random.uniform(0.1, 0.5))

	return {
		"champion": champion.champion,
		"url": champion.url,
		"images": images
	}


class LOLChampionsPage:
	@classmethod
	async def scrap(cls, html_data:HTMLParsed | None = None, url_root: str = "") -> None | list[dict[str, str]]:

		if html_data is None:
			return None

		container = html_data.find('div', attrs={"data-testid": "card-grid"})
		
		if not container:
			return None

		tasks = []
		champions_base = []

		for card in container.find_all('a'):
			url = card.get('href')
			champion = get_champion(card.find('div', attrs={"data-testid": "card-title"}))
			champions_base.append(
				ChampionBase(
					champion = champion,
					url = f"{url_root}{url}"
				)
			)

		tasks = [get_images(champion) for champion in champions_base]
		champions = await asyncio.gather(*tasks)

		return champions
