import os

from typing import Dict

import httpx

from lxml import html

from bs4 import BeautifulSoup


URL:Dict[str, str] = {
	'easport': 'https://www.ea.com/es-es',
	'noticias': 'https://www.ea.com/es-es/news',
	'novedades': 'https://www.ea.com/es-es/games',
	'proximamente' : 'https://www.ea.com/es-es/games/coming-soon',
	'ofertas': 'https://www.ea.com/es-es/sales/deals',
	'gratuitos': 'https://www.ea.com/es-es/games/library/freetoplay'
}


def main():
	pass


if __name__ == '__main__':
	main()