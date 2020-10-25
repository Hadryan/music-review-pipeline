#!/usr/bin/env python
# coding: utf-8

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from string import Template
import pandas as pd

process = CrawlerProcess({'AUTOTHROTTLE_ENABLED': True, 
                          'AUTOTHROTTLE_TARGET_CONCURRENCY': .20,
                          'HTTPCACHE_ENABLED': True,  # remove for final scrape to get live data
                          'ROBOTSTXT_OBEY': True,
                          'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
                          'FEED_URI': '../../data/raw/artists_data.json',
                          'FEED_FORMAT': 'json',
                          'FEED_EXPORT_ENCODING': '"utf-8"'})

class RymArtistSpider(scrapy.Spider):
    name = 'RymArtists'
    pages = range(1, 2)  # set to 25 once multipage is working
    start_yr = 1
    stop_yr = 2  # sb 25 eventually 
    years = range(start_yr, stop_yr)
    starturls = [f"https://rateyourmusic.com/charts/top/album/{year}/{page}"
                 for page in pages for year in years]

    def parse(self, response):
        if response.status == 404:
            return 
        artists_dct = {}
        album_xp = r'//*[@id="content"]/table/tbody/tr/td/table/tbody/'
        artist_xp = r'td[3]/div[1]/div[2]/span/a'
        multiartist_xp = r"td[3]/div[1]/div[2]/span/span[2]/div/div/"
        for album in response.xpath(album_xp):
            # multiple artists e.g. colab:
            if response.xpath(multiartist_xp):
                for mult_artist in album.xpath(mutiartist_xp):
                    artist_name = mult_artist.xpath("@class").get()
                    artist_url = mult_artists.xpath("@href").get()
                    artists_dct[artist_name] = artist_url
            else:
                artist_name = album.xpath(artist_xp+"@class").get()
                artist_url = album.xpath(artist_xp+"@href").get()
            artists_dct[artist_name] = artist_url
        yield artists_dct

process.crawl(RymArtistSpider)
process.start()
