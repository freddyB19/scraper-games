import os
import sys
from typing import Dict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

from utils.main import ReadFromWeb
from utils.main import ReadFromFile

PATH = os.path.join(BASE, "data", "iracing")
FILENAME = "irancing_cars.html"

URL: Dict[str, str] = {
	"cars": "https://www.iracing.com/cars/",
	"tracks": "https://www.iracing.com/tracks/",
	"series": "https://www.iracing.com/series/",
	"seasons": "https://www.iracing.com/seasons/"
}

def get_news(filename: str):
	html = ReadFromFile.read(path_file = os.path.join(PATH, filename))

	container = html.find("div", id="page")

	for new in container.find_all("div", class_="clearfix"):
		tag_h2 = new.find("h2")
		if tag_h2:
			title = tag_h2.find("a").get("title")
			title_url = tag_h2.find("a").get("href")


def get_cars(filename: str):
	html = ReadFromFile.read(path_file = os.path.join(PATH, filename))

	container = html.find("div", id="page")

	for type_car in container.find_all("div", class_="grid-item-search"):

		for car in type_car.find("div", class_="clearfix grid-item-list").css.select("div[data-name]"):
			type = car.get("data-name")
		
			# Otra manera de obtener la Imagen, Url y si es nuevo.
			# container_info_img = car.find("div", class_="grid-item-content-back")
			# container_img = container_info_img.find_all("div")[0]
			# is_new = container_info_img.find_all("div")[1]

			container_img = car.find("div", class_="grid-item-img-container")
			is_new = car.find("div", class_="stick-top-left label-overlay")
			url = container_img.find("a").get("href")
			img = container_img.find("img").get("src")
			is_new_car = True if is_new.find("span") else False
			
			print({"type": type, "url": url, "img": img, "is_new": is_new_car})

		print("---------------------------")


def get_tracks(filename: str):
	html = ReadFromFile.read(path_file = os.path.join(PATH, filename))

	container = html.find("div", id="page")

	list_tracks = container.find("div", class_="row grid-item-list")

	for track in list_tracks.css.select("div[data-name]"):
		track_name = track.get("data-name")
		container_img = track.find("div", class_="grid-item-img-container")
		is_new = True if track.find(
			"div", 
			class_="stick-top-left label-overlay"
		).css.select("span[class*='label-info']") else False
		included = True if track.find(
			"div", 
			class_="stick-top-left label-overlay"
		).css.select("span[class*='label-success']") else False
		url = container_img.find("a").get("href")
		img = container_img.find("img").get("src")

		print({"track": track_name, "url": url, "img": img, "is_new": is_new, "included": included})


def get_series(filename: str):
	html = ReadFromFile.read(path_file = os.path.join(PATH, filename))

	container = html.find("div", id="page")

	for serie in container.css.select("div[class='clearfix']:not(div[id])"):
		name_type_serie = serie.find("h2").get_text().strip()

		print(name_type_serie)

		for type in serie.css.select("div[class='clearfix']:not(div[id]) > div"):
			container = type.find("div", class_="grid-item-content-container")
			container_img = container.find("div", class_="grid-item-img-container")
			url = container_img.find("a").get("href")
			img = container_img.find("a").find("img").get("src")

			container_name_serie = type.find("div", class_="grid-item-content")
			name_serie = container_name_serie.find("span").find("a").string.strip()

			print({"url": url, "img": img, "name_serie": name_serie})

		print("---------------------------")

def get_season(filename: str):
	html = ReadFromFile.read(path_file = os.path.join(PATH, filename))

	container = html.find("div", class_="wp-block-group is-layout-constrained wp-container-core-group-is-layout-2 wp-block-group-is-layout-constrained")

	for season in container.find_all("div", recursive=False):
		img = season.find("img").get("src")
		container_info = season.find("div")

		tags_p = container_info.find_all("p")
		is_latest = True if len(tags_p) == 2 else False

		season = container_info.find("div").find("a").string.strip()
		season_url = container_info.find("div").find("a").get("href")
		season_date = container_info.find('p').find('strong')

		if not season_date:
			season_date = f"{tags_p[1].find('strong').string.strip()}{tags_p[1].get_text().strip()[-1]}"
		else:
			date = container_info.find('p').get_text().strip().replace("\n", "")

			date_format_month_year = tuple(date.split(","))
			month, year = date_format_month_year

			season_date = f"{month}, {year.replace(' ', '')}"
		print({"season": season, "season_url": season_url, "season_date": season_date, "is_latest": is_latest, "img": img})


def main():
	get_season(filename = "iracing_seasons.html")
	
	
if __name__ == '__main__':
	main()