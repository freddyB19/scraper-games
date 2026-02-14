import pprint
from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup


HTMLParsed = TypeVar("HTMLParsed", bound = BeautifulSoup)

def get_image(img: Tag | None) -> str:
	if not isinstance(img, Tag):
		return None

	return img.get("src")

def get_data_season(season: Tag | None) -> str:
	if not isinstance(season, Tag):
		return None

	date = season.find("a")
	return date.get_text().strip() if date else None

def get_data_season_url(season: Tag | None) -> str:
	if not isinstance(season, Tag):
		return None

	url = season.find("a")
	return url.get("href") if url else None

def get_data_season_date(season: Tag | None) -> Tag:
	if not isinstance(season, Tag):
		return None

	return season.find("strong")

def format_season_date(list_tag: list[Tag]) -> str:
	if not list_tag:
		return None

	if not isinstance(list_tag[1], Tag): # Esto es así list_tag[1] debido a que es el resultado que nos interesa
		return None

	tag = list_tag[1]
	content = tag.find('strong')

	if not content:
		return None

	return f"{content.get_text().strip()}{tag.get_text().strip()[-1]}"


def clean_date_format(date: str) -> str:
	clean_date = date.strip().replace("\n", "")
	month, year =  tuple(clean_date.split(","))
	return  f"{month}, {year.replace(' ', '')}"

def format_season_date_2(tag: Tag | None) -> str: 
	if not isinstance(tag, Tag):
		return None

	return clean_date_format(date = tag.get_text())


def get_season(html: HTMLParsed | None):
	if not html:
		return None

	container = html.find("div", class_="wp-block-group is-layout-constrained wp-container-core-group-is-layout-2 wp-block-group-is-layout-constrained")

	if not container:
		return None

	seasons = []
	for season in container.find_all("div", recursive=False):
		image = get_image(season.find("img"))
		container_info = season.find("div")

		tags_p = container_info.find_all("p")
		is_latest = True if len(tags_p) == 2 else False

		season = get_data_season(container_info.find("div")) 
		season_url = get_data_season_url(container_info.find("div"))
		season_date = get_data_season_date(container_info.find('p'))

		if not season_date:
			season_date = format_season_date(tags_p)
		else:
			season_date = format_season_date_2(container_info.find('p'))

		seasons.append({
			"season": season, 
			"season_url": season_url, 
			"season_date": season_date, 
			"is_latest": is_latest, 
			"image": image
		})

	return seasons
