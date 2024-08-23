import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

PLAYLIST_JSON_FILE = os.getenv("PLAYLIST_JSON_FILE")
PLAYLIST_NAME = os.getenv("PLAYLIST_NAME")
PLAYLIST_THUMBNAIL_FOLDER = os.getenv("PLAYLIST_THUMBNAIL_FOLDER")


def save_thumbnail(binary_file_content, file_index: int):
    thumbnail_file_name = f"{PLAYLIST_NAME}_{file_index}.jpg"
    thumbnail_file_path = f"{PLAYLIST_THUMBNAIL_FOLDER}/{thumbnail_file_name}"
    with open(thumbnail_file_path, mode="wb") as file:
        file.write(binary_file_content)
        print(f"saved {thumbnail_file_name} to {thumbnail_file_path}")


def fetch_thumbnails(thumbnail_urls: list):
    for index, thumbnail_url in enumerate(thumbnail_urls, start=1):
        response = requests.get(thumbnail_url)
        response.raise_for_status()
        save_thumbnail(response.content, index)


with open(PLAYLIST_JSON_FILE, mode="r") as playlist_json:
    playlist_data = json.load(playlist_json)
    thumbnail_urls = [
        item["snippet"]["thumbnails"]["maxres"]["url"] for item in playlist_data
    ]
    fetch_thumbnails(thumbnail_urls)
