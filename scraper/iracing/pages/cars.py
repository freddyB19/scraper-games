import pprint
from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound = BeautifulSoup)


def get_data_from_element(element: Tag | None, tag: str, tag_property: str) -> str:
	if not isinstance(element, Tag):
		return None

	html_tag = element.find(tag)
	return html_tag.get(tag_property) if html_tag else None


def valid_is_new_car(car: Tag | None) -> bool:
	if not isinstance(car, Tag):
		return None

	return True if car.find("span") else False

def get_cars(html: HTMLParsed | None):
	if not html:
		return None

	container = html.find("div", id="page")

	if not container:
		return None

	cars = []
	for car in container.css.select('div[class="clearfix grid-item-list"] div[data-name]'):
		type = car.get("data-name")

		container_img = car.find("div", class_="grid-item-img-container")
		url = get_data_from_element(container_img, tag = 'a', tag_property = 'href') 
		image = get_data_from_element(container_img, tag = 'img', tag_property = 'src') 
		is_new_car = valid_is_new_car(car.find("div", class_="stick-top-left label-overlay"))
		
		cars.append({"type": type, "url": url, "image": image, "is_new": is_new_car})

	return cars
