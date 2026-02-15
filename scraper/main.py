import os, json, asyncio

import httpx

from utils.main import async_read_from_web, ASYNC_CLIENT_CONFIG

from lol.main import ScraperLOL
from easport.main import ScraperEASport
from noticias.main import ScraperNoticias
from iracing.main import scraper as async_iracing_scraper

BASE = os.path.dirname(os.path.abspath(__file__))

async def main():
	limits = ASYNC_CLIENT_CONFIG["_LIMITS"]
	headers = ASYNC_CLIENT_CONFIG["_HEADERS"]
	async with httpx.AsyncClient(limits = limits, headers = headers) as client:
		tasks = [
			ScraperLOL.async_scraper(),
			ScraperEASport.async_scraper(),
			ScraperNoticias.async_scraper(),
			async_iracing_scraper()
		]

		lol, easport, news, iracing = await asyncio.gather(
			*tasks, 
			return_exceptions = True
		)


	results = [
		{'page': {'name': 'lol', 'data': lol}},
		{'page': {'name': 'easport', 'data': easport}},
		{'page': {'name': 'noticias', 'data': news}},
		{'page': {'name': 'iracing', 'data': iracing}},
	]

	with open(os.path.join(BASE, 'result.json'), 'w+') as file:
		json.dump(results, file, indent=4)
	

if __name__ == '__main__':
	asyncio.run(main())
