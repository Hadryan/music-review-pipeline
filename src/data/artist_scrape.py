#!/usr/bin/env python
# coding: utf-8

import scrapy
from scrapy.shell import inspect_response
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from string import Template
import pandas as pd

process = CrawlerProcess({'AUTOTHROTTLE_ENABLED': True, 
                          'AUTOTHROTTLE_TARGET_CONCURRENCY': .20,
                          'HTTPCACHE_ENABLED': False,  # remove for final scrape to get live data
                          'ROBOTSTXT_OBEY': False,
                          'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
                          'FEEDS': {'../../data/raw/artists_data.json': {'format': 'json'}},
                          'FEED_EXPORT_ENCODING': '"utf-8"'})

class RymArtistSpider(scrapy.Spider):
    name = 'RymArtists'
    pages = list(range(1, 2))  # set to 25 once multipage is working
    start_yr = 1950
    stop_yr = 1951  # sb 25 eventually 
    start_urls = [f"https://rateyourmusic.com/charts/top/album/{year}/{page}"
                 for page in pages for year in range(1950,1951)]

    def parse(self, response):
        """Parses yearly top album chart pages to obtain artists w/urls"""
        if response.status == 404:
            return 
        artist_xp = r'//a[has-class("artist")/'
        artist_name_xp = artist_xp + 'text()'
        artist_url_xp = artist_xp + '@href'
        artist_names = response.xpath(artist_xp).getall()
        artist_urls = response.xpath(artists_url_xp).getall()
        # scrapy doesn't crawl dups by default, but this will prefilter anyway
        artists_dct = {name: 'rateyourmusic.com/' + url 
                for name, url in zip(artist_names, artist_urls)}
        for artist, artist_url in artists_dict.items():
            yield scrapy.Request(artist_url, callback=artistparse,
                    meta={'artist': artist})

    def artistparse(self, response)
        artist=response.meta.get('artist')


process.crawl(RymArtistSpider)
process.start()
