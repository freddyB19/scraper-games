import os, sys, pprint, asyncio, json
from enum import Enum
from typing import TypeVar

from bs4 import BeautifulSoup

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils.main import (
	run_task,
	DownloadFile, 
	AsyncReadFromWeb,
	AsyncReadFromFile,
)
from lol.pages.lolchampions import LOLChampionsPage 
from lol.pages.news_and_notes import LOLNewsNotesPage

HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)

URLS = {
	'lol': 'https://www.leagueoflegends.com',
	'lolchampions': 'https://www.leagueoflegends.com/es-es/champions/',
	'lolnews': 'https://www.leagueoflegends.com/es-es/news/',
	'lolnotas': 'https://www.leagueoflegends.com/es-es/news/tags/patch-notes/',
}


async def champions() -> list[ dict[str, list[dict[str , str | None]]] ]: 
	content_html = await AsyncReadFromWeb.read(URLS['lolchampions'])
	return await LOLChampionsPage.scrap(
		html_data = content_html,
		url_root = URLS['lol']
	)

async def news() -> list[ dict[str, list[dict[str , str | None]]]]:
	content_html = await AsyncReadFromWeb.read(URLS["lolnews"])
	return await run_task(LOLNewsNotesPage.scrap, content_html)


async def notes() -> list[dict[str, list[dict[str , str | None]]]]:
	content_html = await AsyncReadFromWeb.read(URLS["lolnotas"])
	return await run_task(LOLNewsNotesPage.scrap, content_html, URLS['lol'])


class ScraperLOL:

	@classmethod
	async def async_scraper(cls) -> dict[str, list[dict[str, str | list[str] | None]]]:
		tasks = [news(), notes(), champions()]

		noticias, notas, campeones = await asyncio.gather(*tasks, return_exceptions = True)

		return {
			'champions': campeones if isinstance(campeones, list) else None,
			'noticias': noticias if isinstance(noticias, list) else None,
			'notas': notas if isinstance(notas, list) else None
		}

async def main() -> None:
	result = await ScraperLOL.async_scraper()
	
	pprint.pprint(result)

if __name__ == '__main__':
	asyncio.run(main())
