from lxml import html

from httpx import Client

from bs4 import BeautifulSoup


STATUS_CODE:dict = {
	"OK": 200
}

class ReadFromWeb:
	
	@classmethod
	def read(cls, url:str):
		with Client() as client:
			data = ""
		
			response = client.get(url)

			if response.status_code == STATUS_CODE['OK']:
				data = html.fromstring(response.text)

				html_parsed = BeautifulSoup( html.tostring(data), 'lxml')
				
				return html_parsed
			
			return None



class ReadFromFile:

	@classmethod
	def read(cls, path_file):
		data = None
		with open(path_file, 'r') as file:
			data = file.read()

		return data
