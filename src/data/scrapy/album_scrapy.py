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
    """scrapes individual's numerical ratings of albums, text reviews, and album details"""   
    custom_settings = {  # all needed for splash
        'SPLASH_URL': 'http://192.168.59.103:8050',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,},
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,},
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
                      } 
    name = 'RymAlbum'
    def albumparse(self, response):
        album_name = response.xpath('//div[has-class("album_title")/text()').get()
        artist_name = response.xpath('//a[has-class("artist")/text()').get()
        album_date = response.xpath('//*[contains(text(), "Released")]')
        album_ratings = response.xpath('//script[contains(., 'function drawChart1')]')
