import os, sys, json, asyncio, pprint

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from typing import TypeVar

import httpx

from utils.main import (
	AsyncReadFromFile,
	async_read_from_web,
	ASYNC_CLIENT_CONFIG,
	DownloadFile,
	run_task
)

from iracing.pages.cars import get_cars
from iracing.pages.news import get_news
from iracing.pages.seasons import get_season
from iracing.pages.series import get_series
from iracing.pages.tracks import get_tracks
from iracing.pages.news import get_news


AsyncClient = TypeVar("AsyncClient", bound=httpx.AsyncClient)
MainScraperResult = dict[str, list[dict[str , str | None]]  | str | None  ]
ScraperResult = list[ dict[str, list[dict[str , str | None]]  | str | None  ]]


URL = {
	"cars": "https://www.iracing.com/cars/",
	"tracks": "https://www.iracing.com/tracks/",
	"series": "https://www.iracing.com/series/",
	"seasons": "https://www.iracing.com/seasons/",
	"news": "https://www.iracing.com/category/news/sim-racing-news/"
}

async def scraper_cars(client: AsyncClient) -> ScraperResult:
	content = await async_read_from_web(client = client, url = URL["cars"])
	return await run_task(get_cars, content)

async def scraper_tracks(client: AsyncClient) -> ScraperResult:
	content = await async_read_from_web(client = client, url = URL["tracks"])
	return await run_task(get_tracks, content)

async def scraper_series(client: AsyncClient) -> ScraperResult:
	content = await async_read_from_web(client = client, url = URL["series"])
	return await run_task(get_series, content)

async def scraper_seasons(client: AsyncClient) -> ScraperResult:
	content = await async_read_from_web(client = client, url = URL["seasons"])
	return await run_task(get_season, content)

async def scraper_news(client: AsyncClient) -> ScraperResult:
	content = await async_read_from_web(client = client, url = URL["news"])
	return await run_task(get_news, content)

async def scraper() -> MainScraperResult:
	limits = ASYNC_CLIENT_CONFIG["_LIMITS"]
	headers = ASYNC_CLIENT_CONFIG["_HEADERS"]
	async with httpx.AsyncClient(limits = limits, headers = headers) as client:
		tasks = [
			scraper_cars(client),
			scraper_tracks(client),
			scraper_series(client),
			scraper_seasons(client),
			scraper_news(client)
		]

		cars, tracks, series, seasons, news = await asyncio.gather(
			*tasks, 
			return_exceptions = True
		)

	return {
		"cars": cars, 
		"tracks": tracks, 
		"series": series, 
		"seasons": seasons, 
		"news": news
	}


async def main():
	result = await scraper()

	pprint.pprint(result, indent = 4)
	
if __name__ == '__main__':
	asyncio.run(main())


__all__ = ["scraper"]