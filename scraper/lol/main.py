import os, sys, pprint, asyncio, json
from typing import TypeVar

import httpx

from bs4 import BeautifulSoup


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils import check_result
from utils.main import (
	run_task,
	DownloadFile, 
	AsyncReadFromWeb,
	AsyncReadFromFile,
	async_read_from_web,
	ASYNC_CLIENT_CONFIG

)

from lol.pages.lolchampions import LOLChampionsPage 
from lol.pages.news_and_notes import LOLNewsNotesPage

HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)
AsyncClient = TypeVar("AsyncClient", bound=httpx.AsyncClient)

URLS = {
	'lol': 'https://www.leagueoflegends.com',
	'lolchampions': 'https://www.leagueoflegends.com/es-es/champions/',
	'lolnews': 'https://www.leagueoflegends.com/es-es/news/',
	'lolnotas': 'https://www.leagueoflegends.com/es-es/news/tags/patch-notes/',
}


async def champions(client: AsyncClient) -> list[ dict[str, list[dict[str , str | None]]] ]:
	content_html = await async_read_from_web(client = client, url = URLS["lolchampions"])
	return await LOLChampionsPage.scrap(
		html_data = content_html,
		url_root = URLS['lol']
	)

async def news(client: AsyncClient) -> list[ dict[str, list[dict[str , str | None]]]]:
	content_html = await async_read_from_web(client = client, url = URLS["lolnews"])
	return await run_task(LOLNewsNotesPage.scrap, content_html)


async def notes(client: AsyncClient) -> list[dict[str, list[dict[str , str | None]]]]:
	content_html = await async_read_from_web(client = client, url = URLS["lolnotas"])
	return await run_task(LOLNewsNotesPage.scrap, content_html, URLS['lol'])


class ScraperLOL:

	@classmethod
	async def async_scraper(cls) -> dict[str, list[dict[str, str | list[str] | None]]]:
		async with httpx.AsyncClient(limits = ASYNC_CLIENT_CONFIG["_LIMITS"], headers = ASYNC_CLIENT_CONFIG["_HEADERS"]) as client:
			tasks = [news(client), notes(client), champions(client)]

			noticias, notas, campeones = await asyncio.gather(*tasks, return_exceptions = True)

		return {
			'champions': check_result(campeones, scraper = "lol.campeones"),
			'noticias': check_result(noticias, scraper = "lol.noticias"),
			'notas': check_result(notas, scraper = "lol.notas"),
		}

async def main() -> None:
	result = await ScraperLOL.async_scraper()
	
	pprint.pprint(result)

if __name__ == '__main__':
	asyncio.run(main())
