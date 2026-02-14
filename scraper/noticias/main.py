import os, sys, pprint, json, asyncio
from typing import TypeVar

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

import httpx

from utils.main import (
	ReadFromWeb, 
	ReadFromFile, 
	DownloadFile, 
	run_task,
	async_read_from_web,
	ASYNC_CLIENT_CONFIG
)

from noticias.pages.marca import MarcaNoticias
from noticias.pages.lanacion import LaNacionNoticias
from noticias.pages.wired import get_news, get_robots_news


AsyncClient = TypeVar("AsyncClient", bound=httpx.AsyncClient)
ScraperResult = list[ dict[str, list[dict[str , str | None]]] ]

URL = {
	'lanacion': 'https://www.lanacion.com.ar/tema/videojuegos-tid48572/', 
	'lanacion_tecnologia': 'https://www.lanacion.com.ar/tecnologia/',
	'marca': 'https://www.marca.com/videojuegos/juegos.html?intcmp=MENUMIGA&s_kw=juegos',
	'wired_espacio': 'https://es.wired.com/ciencia/espacio',
	'wired_biotecnologia': 'https://es.wired.com/ciencia/biotecnologia',
	'wired_neurociencia': 'https://es.wired.com/ciencia/neurociencia',
	'wired_robots': 'https://es.wired.com/tag/robots',
}

async def asyn_marca(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['marca'])
	return await run_task(MarcaNoticias.scrap, content_html)

async def asyn_lanacion(client: AsyncClient, url_root:str = 'https://www.lanacion.com.ar/') -> ScraperResult:
	content_html = await async_read_from_web(client, URL['lanacion'])
	return await run_task(LaNacionNoticias.scrap, content_html, url_root)

async def asyn_lanacion_tecnologia(client: AsyncClient, url_root:str = 'https://www.lanacion.com.ar/') -> ScraperResult:
	content_html = await async_read_from_web(client, URL['lanacion_tecnologia'])
	return await run_task(LaNacionNoticias.scrap, content_html, url_root)

async def asyn_wired_espacio(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['wired_espacio'])
	return await run_task(get_news, content_html, URL['wired_espacio'])

async def asyn_wired_biotecnologia(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['wired_biotecnologia'])
	return await run_task(get_news, content_html, URL['wired_biotecnologia'])

async def asyn_wired_neurociencia(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['wired_neurociencia'])
	return await run_task(get_news, content_html, URL['wired_neurociencia'])

async def asyn_wired_robots(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['wired_robots'])
	return await run_task(get_robots_news, content_html, URL["wired_robots"])

def marca() -> ScraperResult:
	return MarcaNoticias.scrap( 
		html_parsed = ReadFromWeb.read(URL['marca'])
	)

def lanacion() -> ScraperResult:
	return LaNacionNoticias.scrap(
		html_parsed = ReadFromWeb.read(URL['lanacion']),
		url_root = 'https://www.lanacion.com.ar/'
	)

def lanacion_tecnologia() -> ScraperResult:
	return LaNacionNoticias.scrap(
		html_parsed = ReadFromWeb.read(URL['lanacion_tecnologia']),
		url_root = 'https://www.lanacion.com.ar/'
	)

def wired_robots() -> ScraperResult:
	return get_robots_news(
		html_parsed = ReadFromWeb.read(URL["wired_robots"]),
		url_root = URL["wired_robots"]
	)

def wired_neurociencia() -> ScraperResult:
	return get_news(
		html_parsed = ReadFromWeb.read(URL["wired_neurociencia"]), 
		url_root = URL["wired_neurociencia"]
	)

def wired_biotecnologia() -> ScraperResult:
	return get_news(
		html_parsed = ReadFromWeb.read(URL["wired_biotecnologia"]), 
		url_root = URL["wired_biotecnologia"]
	)

def wired_espacio() -> ScraperResult:
	return get_news(
		html_parsed = ReadFromWeb.read(URL["wired_espacio"]), 
		url_root = URL["wired_espacio"]
	)

class ScraperNoticias:

	@classmethod
	async def async_scraper(cls):
		async with httpx.AsyncClient(limits = ASYNC_CLIENT_CONFIG["_LIMITS"], headers = ASYNC_CLIENT_CONFIG["_HEADERS"]) as client:
			tasks = [
				asyn_marca(client),
				asyn_lanacion(client),
				asyn_lanacion_tecnologia(client),
				asyn_wired_espacio(client),
				asyn_wired_biotecnologia(client),
				asyn_wired_neurociencia(client),
				asyn_wired_robots(client)
			]

			results = await asyncio.gather(*tasks, return_exceptions = True)

			marca = results[0] if isinstance(results[0], list) else None
			lanacion = results[1] if isinstance(results[1], list) else None
			lanacion_tecnologia = results[2] if isinstance(results[2], list) else None
			wired_espacio = results[3] if isinstance(results[3], list) else None
			wired_biotecnologia = results[4] if isinstance(results[4], list) else None
			wired_neurociencia = results[5] if isinstance(results[5], list) else None
			wired_robots = results[6] if isinstance(results[6], list) else None

		return [
			{'nombre': 'marca', 'pagina':  marca},
			{
				'nombre': 'la nación', 
				'pagina': lanacion,
				'subs': [
					{
						'nombre': 'la nación tecnología', 
						'pagina': lanacion_tecnologia
					}
				]
			},
			{
				'nombre': 'wired',
				'subs': [
					{
						'nombre': 'wired robots',
						'pagina': wired_robots
					},
					{
						'nombre': 'wired neurociencia',
						'pagina': wired_neurociencia
					},
					{
						'nombre': 'wired biotecnología',
						'pagina': wired_biotecnologia
					},
					{
						'nombre': 'wired espacio',
						'pagina': wired_espacio
					},

				]
			}
		]

	@classmethod
	def scraper(cls) -> ScraperResult:

		return [
			{'nombre': 'marca', 'pagina': marca()},
			{
				'nombre': 'la nación', 
				'pagina': lanacion(),
				'subs': [
					{
						'nombre': 'la nación tecnología', 
						'pagina': lanacion_tecnologia()
					}
				]
			},
			{
				'nombre': 'wired',
				'subs': [
					{
						'nombre': 'wired robots',
						'pagina': wired_robots()
					},
					{
						'nombre': 'wired neurociencia',
						'pagina': wired_neurociencia()
					},
					{
						'nombre': 'wired biotecnologia',
						'pagina': wired_biotecnologia()
					},
					{
						'nombre': 'wired spacio',
						'pagina': wired_espacio()
					},

				]
			}
		]

async def main():
	pprint.pprint(await ScraperNoticias.async_scraper(), indent = 4)

if __name__ == '__main__':
	asyncio.run(main())
