import pprint
from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound = BeautifulSoup)


def get_data_from_element(list_tag: list[Tag], tag_property: str) -> str:
	if not list_tag:
		return None

	if not isinstance(list_tag[0], Tag):
		return None

	element = list_tag[0]
	return element.get(tag_property)


def get_tracks(html: HTMLParsed | None):
	if not html:
		return None

	container = html.find("div", id="page")

	if not container:
		return None

	tracks = []

	CSS_SELECT_CONTAINER = 'div[class*="row grid-item-list"] div[data-name]'
	CSS_SELECT_IS_NEW = 'div[class="stick-top-left label-overlay"] span[class*="label-info"]'
	CSS_SELECT_INCLUDED = 'div[class="stick-top-left label-overlay"] span[class*="label-success"]'

	for track in container.css.select(CSS_SELECT_CONTAINER):
		track_name = track.get("data-name")
		image = get_data_from_element(
			track.css.select('div[class="grid-item-img-container"] img'),
			tag_property = "src"
		)
		url = get_data_from_element(
			track.css.select('div[class="grid-item-img-container"] a'),
			tag_property = "href"
		)
		is_new = True if track.css.select(CSS_SELECT_IS_NEW) else False
		included = True if track.css.select(CSS_SELECT_INCLUDED) else False

		tracks.append({
			"track": track_name, 
			"url": url, 
			"image": image, 
			"is_new": is_new, 
			"included": included
		})

	return tracks
