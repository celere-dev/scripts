#!/usr/bin/env python3
"""Recupera a quantidade de ocorrências de chamada para "https://datawrapper.dwcdn.net"
em um post do WordPress e salva o resultado (ID, data, link e quantidade de ocorrências) em um TXT,
de acordo com o idioma.
"""
__version__ = "0.1"
__author__ = "Claromes <claromes@celere.dev>"


import requests
import re

DOMAIN = input("Domain: ")


def count_src(content):
    return len(re.findall(r'src="https://datawrapper\.dwcdn\.net[^"]*"', content))


langs = ["pt", "es", "en"]

for lang in langs:
    base_url = f"https://{DOMAIN}/wp-json/wp/v2/posts"
    page = 1
    result = []

    while True:
        response = requests.get(
            base_url, params={"lang": lang, "per_page": 100, "page": page}
        )
        print(response.url)
        if response.status_code != 200 or not response.json():
            break

        posts = response.json()

        for post in posts:
            count = count_src(post["content"]["rendered"])
            if count >= 2:
                result.append(
                    f"id: {post['id']}, date: {post['date']}, link: {post['link']}, src: {count}"
                )

        page += 1

    with open(f"datawrapper_count_src_{lang}.txt", "w") as f:
        f.write("\n".join(map(str, result)))
