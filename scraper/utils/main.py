import logging

from typing import Union, TypeVar, Dict, Any

from lxml import html, etree

from httpx import Client, ConnectError

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


class ReadFromFile:

	@classmethod
	def read(cls, path_file):
		data: HTMLParsed | None = None
		with open(path_file, 'r') as file:
			file = file.read()

			data = BeautifulSoup( file, 'lxml')

		return data


class DownloadFile:

	@classmethod
	def init(cls, url: str, path_for_save: str) -> Dict[str, bool | Any ]:
		html = ReadFromWeb.read(url = url)
		if not html:
			return {"state": False, "data": html}
		with open(path_for_save, "a") as file:
			file.write(html.prettify())

		return {"state": True, "data": html}
		

		
