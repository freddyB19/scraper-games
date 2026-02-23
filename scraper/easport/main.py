import os, sys, json, pprint, asyncio, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

import httpx

from utils import check_result
from utils.main import (
	run_task,
	ReadFromWeb,
	ReadFromFile,
	AsyncReadFromFile,

	async_read_from_web,
	ASYNC_CLIENT_CONFIG
)

from easport.pages.noticias import NoticiasEASport
from easport.pages.novedades import NovedadesEASport
from easport.pages.gratuitos import JuegoGratuitosEASport
from easport.pages.proximamente import ProximamenteEASport
from easport.pages.actualizaciones import ActualizacionesEASport

URL = {
	'easport': 'https://www.ea.com/es-es',
	'noticias': 'https://www.ea.com/es-es/news',
	'novedades': 'https://www.ea.com/es-es/games',
	'proximamente' : 'https://www.ea.com/es-es/games/coming-soon',
	'gratuitos': 'https://www.ea.com/es-es/games/library/freetoplay'
}

def sync_easport_news():
	return NoticiasEASport.scrap(
		html_data = ReadFromWeb.read(URL["noticias"])
	)

def sync_easport_novelties(url_root:str = "https://www.ea.com"):
	return NovedadesEASport.scrap(
		html_data = ReadFromWeb.read(URL["novedades"]),
		url_root = url_root
	)

def sync_easport_soon():
	return ProximamenteEASport.scrap(
		html_data = ReadFromWeb.read(URL["proximamente"])
	)

def sync_easport_free(url_root:str = "https://www.ea.com"):
	return JuegoGratuitosEASport.scrap(
		html_data = ReadFromWeb.read(URL["gratuitos"]),
		url_root = url_root
	)

def sync_easport_updates():
	return ActualizacionesEASport.scrap(
		html_data = ReadFromWeb.read(URL["easport"])
	)

async def easport_news(client) -> list[dict[str, str | None]] | None:
	content_html = await async_read_from_web(client, URL["noticias"])
	return await run_task(NoticiasEASport.scrap, content_html)

async def easport_novelties(client, url_root = "https://www.ea.com"):
	content_html = await async_read_from_web(client, URL["novedades"])
	return await run_task(NovedadesEASport.scrap, content_html, url_root)

async def easport_soon(client):
	content_html = await async_read_from_web(client, URL["proximamente"])
	return  await run_task(ProximamenteEASport.scrap, content_html)

async def easport_free(client, url_root = "https://www.ea.com"):
	content_html = await async_read_from_web(client, URL["gratuitos"])
	return await run_task(JuegoGratuitosEASport.scrap, content_html, url_root)

async def easport_updates(client):
	content_html = await async_read_from_web(client, URL["easport"])
	return await run_task(ActualizacionesEASport.scrap, content_html)

class ScraperEASport:

	@classmethod
	async def async_scraper(cls):
		async with httpx.AsyncClient(limits = ASYNC_CLIENT_CONFIG["_LIMITS"], headers = ASYNC_CLIENT_CONFIG["_HEADERS"]) as client:
			tasks = [
				easport_news(client = client),
				easport_novelties(client = client),
				easport_soon(client = client),
				easport_free(client = client),
				easport_updates(client = client)
			]

			news, novelties, soon, free, updates = await asyncio.gather(*tasks, return_exceptions = True)

		return {
			'noticias': check_result(news, scraper="news"), #if isinstance(news, list) else None,
			'novedades': check_result(novelties, scraper="novelties"), #if isinstance(novelties, list) else None,
			'proximamente': check_result(soon, scraper="soon"), #if isinstance(soon, list) else None,
			'gratuitos': check_result(free, scraper="free"), #if isinstance(free, list) else None,
			'actualizaciones': check_result(updates, scraper="updates") #if isinstance(updates, list) else None
		}

	@classmethod
	def scraper(cls):
		data_news = sync_easport_news()
		data_novelties = sync_easport_novelties()
		data_soon = sync_easport_soon()
		data_free = sync_easport_free()
		data_updates = sync_easport_updates()
		
		return {
			'noticias': data_news,
			'novedades': data_novelties,
			'proximamente': data_soon,
			'gratuitos': data_free,
			'actualizaciones': data_updates,
		}

async def main():
	# Time: 1.87
	start = time.perf_counter()
	pprint.pprint(await ScraperEASport.async_scraper(), indent = 4)
	print(f"Time: {time.perf_counter() - start}")


if __name__ == '__main__':
	asyncio.run(main())
