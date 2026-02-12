import logging, asyncio

from typing import Union, TypeVar, Dict, Any

from lxml import html, etree

import httpx
from httpx import Client, ConnectError

import aiofiles

from bs4 import BeautifulSoup


Request = TypeVar("Request", bound=Client)
Parsed = TypeVar("Parsed", bound=etree.Element)
HTMLParsed = TypeVar("HTMLParsed", bound=BeautifulSoup)

STATUS_CODE = {
	"OK": 200
}

FORMAT = "%(asctime)s %(error)s %(url)s %(message)s"

logging.getLogger(__name__)
logging.basicConfig(format = FORMAT)

class ReadFromWeb:
	
	@classmethod
	def read(cls, url:str) -> HTMLParsed | None:
		try:
			with Client() as client:
		
				response:Request = client.get(url)

				if response.status_code == STATUS_CODE['OK']:
					data:Parsed = html.fromstring(response.text)

					html_parsed:HTMLParsed = BeautifulSoup( html.tostring(data), 'lxml')
					
					return html_parsed
				
				return None
		except ConnectError as e:
			logging.error("Error en la extracción", extra = {"error": str(e), "url": url})
			return None


MAX_REQUEST = 10
MAX_CONCURRENT_REQUEST = 5
class AsyncReadFromWeb:
	_SEMAPHORE = asyncio.Semaphore(MAX_CONCURRENT_REQUEST)
	_LIMITS = httpx.Limits(
		max_keepalive_connections = MAX_CONCURRENT_REQUEST, # límite de conexiones "activas" permitidas 
		max_connections = MAX_REQUEST # límite de conexiones permitidas
	)
	_TIMEOUT = 10.0
	_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
	
	@classmethod
	async def read(cls, url:str) -> HTMLParsed | None:
		async with cls._SEMAPHORE:
			try:
				async with httpx.AsyncClient(limits = cls._LIMITS, headers = cls._HEADERS) as client:
				 	response = await client.get(url, timeout=cls._TIMEOUT)

				if response.status_code == STATUS_CODE['OK']:
					data = html.fromstring(response.text)

					html_parsed = BeautifulSoup( html.tostring(data), 'lxml')
					
					return html_parsed
				
				return None
			except ConnectError as e:
				logging.error("Error en la extracción", extra = {"error": str(e), "url": url})
				return None


class ReadFromFile:

	@classmethod
	def read(cls, path_file):
		with open(path_file, 'r') as file:
			file = file.read()

			data = BeautifulSoup( file, 'lxml')

		return data


class AsyncReadFromFile:

	@classmethod
	async def read(cls, path_file):
		async with aiofiles.open(path_file, 'r') as file:
			file = await file.read()

		return BeautifulSoup( file, 'lxml')


class DownloadFile:

	@classmethod
	def init(cls, url: str, path_for_save: str) -> Dict[str, bool | Any ]:
		html = ReadFromWeb.read(url = url)
		if not html:
			return {"state": False, "data": html}
		with open(path_for_save, "a") as file:
			file.write(html.prettify())

		return {"state": True, "data": html}
		

async def run_task(func, *args):	
	loop = asyncio.get_running_loop()
	content = await loop.run_in_executor(None, func, *args)

	return content
