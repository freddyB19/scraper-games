import pprint
from typing import TypeVar

from bs4.element import Tag
from bs4 import BeautifulSoup

HTMLParsed = TypeVar("HTMLParsed", bound = BeautifulSoup)

def get_title(title: Tag| None) -> str:
	if not isinstance(title, Tag):
		return None

	return title.get("title").strip()

def get_url(url: Tag| None) -> str:
	if not isinstance(url, Tag):
		return None

	return url.get("href")

def get_image(tag: Tag | None) -> str:
	if not isinstance(tag, Tag):
		return None

	img = tag.find("img")

	return img.get("src") if img else None


def format_date(date: str) -> str:
	str_date,_,_ = date.partition("by")
	return str_date.strip()

def get_date(list_tag: list[Tag]) -> str:
	if not list_tag:
		return None

	if not isinstance(list_tag[0], Tag):
		return None

	date = list_tag[0]

	return format_date(date.get_text())

def get_author(list_tag: list[Tag]) -> str:
	if not list_tag:
		return None
	if not isinstance(list_tag[0], Tag):
		return None

	author = list_tag[0]
	return author.get_text().strip().replace("\n", "")

def get_author_link(list_tag: list[Tag]) -> str:
	if not list_tag:
		return None
	if not isinstance(list_tag[0], Tag):
		return None

	author_link = list_tag[0]
	return author_link.get("href")

def clean_detail(detail: str) -> str:
	return detail.strip().replace("Read the Rest »", "").replace("\n", "").replace("  ", "")

def get_detail(list_tag: list[Tag]):
	if not list_tag:
		return None
	if not isinstance(list_tag[0], Tag):
		return None

	detail = list_tag[0]
	return clean_detail(detail.get_text())


def get_news(html: HTMLParsed | None):
	if not html:
		return None

	container = html.find("div", id="page")

	if not container:
		return None

	news = []

	for new in container.find_all("div", class_="clearfix"):
		if new.find("h2"):
			title = get_title(new.find("a"))
			url = get_url(new.find("a"))
			image = get_image(new.find("a"))
			date =  get_date(new.css.select("p > small"))
			author = get_author(new.css.select("p > small > a"))
			author_link = get_author_link(new.css.select("p > small > a"))
			detail = get_detail(new.css.select("p:not(:has(> small))"))

			news.append({
				"title": title,
				"url": url,
				"image": image,
				"author": {"name": author, "url": author_link},
				"detail": detail,
				"date": date
			})

	return news