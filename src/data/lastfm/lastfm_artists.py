#/usr/bin/python
import requests
import json

class LfmArtists(object):
    """gets artist ratings from users previously identified"""
    def __init__(self):
        self.api_key = input('Last.fm Dev API Key')
        self.url = {'payload': {}, 'headers': {}}
        self.url['root'] = r'http://ws.audioscrobbler.com/2.0/'
        self.url['payload']['method'] = 'user.getTopAlbums'
        self.url['payload']['api_key'] = f'{self.api_key}'
        self.url['payload']['format'] = 'json'
        self.url['payload']['limit'] = 50
        self.url['payload']['period'] = 'overall'
        self.url['headers']['user-agent'] = 'chrisoyer_my-app.0.0.1alpha'
        self.crawled = []
        self.userqueue = []
    def load_users_from_file(self):
        """loads users from file"""
        pass
    def load_users_from_db(self):     
         """loads users from db"""
        pass
    def get_artists(self):
        """pulls data"""
~
