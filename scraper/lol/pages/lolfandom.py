from typing import List
from typing import Dict
from typing import NewType

from bs4 import BeautifulSoup


HTMLParsed = NewType("HTMLParsed", BeautifulSoup)

class LOLFandomPage:

	@classmethod
	def scrap(cls, html_data:HTMLParsed | None = None, url_root: str = "") -> str | List[Dict[str, str]]:

		if html_data is None:
			return None

		columns = html_data.css.select('table[class*="wikitable"] tr[style!=""]')

		if not columns:
			return None

		tabla = []
		
		tags_estadisticas = {
			"0":"HP", 
			"1":"HP+", 
			"2":"HP5", 
			"3":"HP5+", 
			"4":"MP", 
			"5":"MP+",
			"6":"MP5",
			"7":"MP5+",
			"8":"AD",
			"9":"AD+",
			"10":"AS",
			"11":"AS+",
			"12":"AR",
			"13":"AR+",
			"14":"MR",
			"15":"MR+",
			"16":"MS"
		}
		
		for index, column in enumerate(columns[1:]):
			fila = column.td
			
			filas = list(filter(lambda tag: tag.string and len(tag.string) > 2 and not tag.find('strong'), column.find_all('td', style=False)))

			if not filas:
				continue
			
			estadisticas = enumerate(filas)

			champion_estadisticas = list(
				map(
					lambda data: (tags_estadisticas[str(data[0])], data[1].string.strip()) if data[1].string else (tags_estadisticas[str(data[0])], ""), 
					estadisticas
				)
			)

			url_imagen = fila.find('img').get('data-src')

			imagen_info = url_imagen.partition(".png")
			
			heroe = {
				'nombre': fila.find('span', style=True).string.strip(),
				'url': f"{url_root}{fila.find('a', title=True).get('href')}",
				'imagen': f"{imagen_info[0]}{imagen_info[1]}" if imagen_info[1] != '' else imagen_info[0],
				'estadisticas': champion_estadisticas 
			}

			tabla.append(heroe)

		return tabla
