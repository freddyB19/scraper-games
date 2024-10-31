import httpx
from lxml import html
from bs4 import BeautifulSoup


def main():
	response = httpx.get('https://decrypt.co/es/news/artificial-intelligence')

	if response.status_code == 200:
		html_string = html.fromstring(response.text)
		html_parsed = BeautifulSoup(html.tostring(html_string), 'lxml')

		print("Success")
		print(html_parsed.prettify())

	else:
		print(f"Error: {response.status_code}")
		print(BeautifulSoup(html.tostring(html.fromstring(response.text)), 'lxml').prettify())

if __name__ == '__main__':
	main()

# git branch -c | -C albion noticias