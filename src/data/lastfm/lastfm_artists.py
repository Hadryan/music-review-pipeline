#/usr/bin/python
import requests
import json
from glob import glob
import os
from re import search as re_search

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
        os.chdir("../../../data/raw/unprocessed/")
        user_files = glob("lfm_users*.json")
        users_regex = "lfm_users\.(\d+)\-(\d+)\-(\d+)T(\d{6})\.json"
        filenames = [os.path.basename(f)) for f in user_files]
        filedata = [self._open_userjson(filename) for filename in filenames]
        

        os.chdir("../../../src/data/lastfm/")
    @staticmethod
    def _open_userjson(filepath):
        with open(filename, 'f') as f:
            user_data = json.load(f)
            return user_data
    def load_users_from_db(self):     
         """loads users from db"""
        pass
    def get_artists(self):
        """pulls data"""
        resp = requests.get(self.url['root'], params=payload, headers= 
    def to_json(self):
        """saves new artist data to json"""
        pass
    def to_db(self):
        """loads new artist data to db"""
        pass
