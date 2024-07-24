# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:00:08 2024

@author: harivonyratefiarison
"""

from Class.Crawler import Crawler

crawler = Crawler(max_pages=10)
crawler.run('https://dota2.fandom.com/wiki/Dota_2_Wiki')