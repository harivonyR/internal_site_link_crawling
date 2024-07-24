# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:00:35 2024

@author: harivonyratefiarison
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class Crawler:
    def __init__(self, max_pages):
        self.max_pages = max_pages
        self.urls_to_visit = []
        self.visited_urls = []

    def valid_url(self, url):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                return soup
            else:
                print(f"Erreur {r.status_code} avec l'URL {url}")
                return None
        except requests.RequestException as e:
            print(f"Exception lors de la requête de l'URL {url}: {e}")
            return None

    def get_domain(self, url):
        domain = re.search(r"https?://(www\.)?([a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+)", url)
        if domain:
            return domain.group(2)
        return None

    def get_internal_urls(self, url):
        soup = self.valid_url(url)
        if not soup:
            return []

        domain = self.get_domain(url)
        internal_urls = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/'):
                href = urljoin(url, href)
            if domain in href and href not in self.visited_urls and href not in self.urls_to_visit:
                internal_urls.append(href)

        return internal_urls

    def add_urls_to_visit(self, internal_urls):
        for url in internal_urls:
            if url not in self.urls_to_visit and url not in self.visited_urls:
                self.urls_to_visit.append(url)

    def run(self, start_url):
        self.urls_to_visit.append(start_url)

        while self.urls_to_visit and len(self.visited_urls) < self.max_pages:
            url = self.urls_to_visit.pop(0)
            print(f"Exploration de l'URL: {url}")

            internal_urls = self.get_internal_urls(url)
            self.add_urls_to_visit(internal_urls)
            self.visited_urls.append(url)

        print(f"Exploration terminée. {len(self.visited_urls)} pages visitées.")


if __name__ == '__main__' :
    crawler = Crawler(max_pages=10)
    crawler.run('https://dota2.fandom.com/wiki/Dota_2_Wiki')


