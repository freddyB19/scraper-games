from typing import Union
from typing import NewType
from typing import Dict
from typing import Any

from lxml import html

from httpx import Client

from bs4 import BeautifulSoup


Request = NewType("Request", Client)
Parsed = NewType("Parsed", html)
HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

STATUS_CODE:Dict[str, int] = {
	"OK": 200
}

class ReadFromWeb:
	
	@classmethod
	def read(cls, url:str) -> HTMLParsed | None:
		with Client() as client:
		
			response:Request = client.get(url)

			if response.status_code == STATUS_CODE['OK']:
				data:Parsed = html.fromstring(response.text)

				html_parsed:HTMLParsed = BeautifulSoup( html.tostring(data), 'lxml')
				
				return html_parsed
			
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
		

		
