#!/usr/bin/env python3
"""Recupera posts antigos com limite de caracteres
e salva o resultado (ID, data, link, mídias e quantidade de caracteres) em um JSON.
"""
__version__ = "0.1"
__author__ = "Claromes <claromes@celere.dev>"


import requests
import json
from bs4 import BeautifulSoup


DOMAIN = input("Domain: ")
CHARACTERS_LIMIT = 300


def clean_content(content):
    return BeautifulSoup(content, "html.parser").get_text()


def extract_medias(content):
    soup = BeautifulSoup(content, "html.parser")

    medias = []

    for img in soup.find_all("img"):
        if img.get("src"):
            guid = (
                "https://infoamazonia.org" + img["src"]
                if not img["src"].startswith(("http://", "https://"))
                else img["src"]
            )

            img_id = None
            classes = img.get("class", [])
            for class_name in classes:
                if "wp-image-" in class_name:
                    img_id = class_name.split("wp-image-")[1]
                    img_link = f"https://infoamazonia.org/wp-json/wp/v2/media/{img_id}"
                    break

            if img_id:
                medias.append({"id": img_id, "link": img_link, "guid": guid})

    return medias


langs = ["pt", "es", "en"]

for lang in langs:
    base_url = f"https://{DOMAIN}/wp-json/wp/v2/posts"
    id = 1
    page = 1
    result = []

    while True:
        response = requests.get(
            base_url,
            params={
                "lang": lang,
                "before": "2016-12-31T23:59:59",
                "per_page": 100,
                "page": page,
            },
        )
        print(response.url)
        if response.status_code != 200 or not response.json():
            break

        posts = response.json()

        for post in posts:
            content = clean_content(post["content"]["rendered"])

            if len(content) <= CHARACTERS_LIMIT:
                medias = extract_medias(post["content"]["rendered"])

                result.append(
                    {
                        "id": id,
                        "post_id": post["id"],
                        "date": post["date"],
                        "link": post["link"],
                        "medias": medias,
                        "characters": len(content),
                    }
                )

                id += 1

        page += 1

    with open(f"old_posts_by_character_limit_{lang}.json", "w") as f:
        f.write(json.dumps(result, indent=4))
