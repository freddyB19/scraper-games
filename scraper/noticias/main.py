import os, sys, pprint, json, asyncio
from typing import TypeVar

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

import httpx

from utils import check_result
from utils.main import (
	AsyncReadFromFile, 
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

async def async_marca(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['marca'])
	return await run_task(MarcaNoticias.scrap, content_html)

async def async_lanacion(client: AsyncClient, url_root:str = 'https://www.lanacion.com.ar/') -> ScraperResult:
	content_html = await async_read_from_web(client, URL['lanacion'])
	return await run_task(LaNacionNoticias.scrap, content_html, url_root)

async def async_lanacion_tecnologia(client: AsyncClient, url_root:str = 'https://www.lanacion.com.ar/') -> ScraperResult:
	content_html = await async_read_from_web(client, URL['lanacion_tecnologia'])
	return await run_task(LaNacionNoticias.scrap, content_html, url_root)

async def async_wired_espacio(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['wired_espacio'])
	return await run_task(get_news, content_html, URL['wired_espacio'])

async def async_wired_biotecnologia(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['wired_biotecnologia'])
	return await run_task(get_news, content_html, URL['wired_biotecnologia'])

async def async_wired_neurociencia(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['wired_neurociencia'])
	return await run_task(get_news, content_html, URL['wired_neurociencia'])

async def async_wired_robots(client: AsyncClient) -> ScraperResult:
	content_html = await async_read_from_web(client, URL['wired_robots'])
	return await run_task(get_robots_news, content_html, URL["wired_robots"])


class ScraperNoticias:

	@classmethod
	async def async_scraper(cls):
		async with httpx.AsyncClient(limits = ASYNC_CLIENT_CONFIG["_LIMITS"], headers = ASYNC_CLIENT_CONFIG["_HEADERS"]) as client:
			tasks = [
				async_marca(client),
				async_lanacion(client),
				async_lanacion_tecnologia(client),
				async_wired_espacio(client),
				async_wired_biotecnologia(client),
				async_wired_neurociencia(client),
				async_wired_robots(client)
			]

			page_marca, page_lanacion, lanacion_tec, wired_es, wired_bio, wired_neuro, wired_rb= await asyncio.gather(
				*tasks, 
				return_exceptions = True
			)

			marca = check_result(page_marca, "marca") #page_marca if isinstance(page_marca, list) else None
			lanacion = check_result(page_lanacion, "lanacion") #page_lanacion if isinstance(page_lanacion, list) else None
			lanacion_tecnologia = check_result(lanacion_tec, "lanacion-tec") #lanacion_tec if isinstance(lanacion_tec, list) else None
			wired_espacio = check_result(wired_es, "wired-espacio") #wired_es if isinstance(wired_es, list) else None
			wired_biotecnologia = check_result(wired_bio, "wired-biotec") #wired_bio if isinstance(wired_bio, list) else None
			wired_neurociencia = check_result(wired_neuro, "wired-neuroc") #wired_neuro if isinstance(wired_neuro, list) else None
			wired_robots = check_result(wired_rb, "wired-robots") #wired_rb if isinstance(wired_rb, list) else None

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


async def main():
	result = await ScraperNoticias.async_scraper()
	pprint.pprint(result, indent = 4)


if __name__ == '__main__':
	asyncio.run(main())
