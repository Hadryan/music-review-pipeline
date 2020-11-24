#!/usr/bin/python/
import requests
import json
from dataclasses import dataclass, asdict
from dataclasses_json import dataclass_json
from collections import deque
from random import randint
from time import sleep
from typing import Optional
from datetime import datetime

@dataclass_json
@dataclass
class LfmUserData():
    """dataclass to store retrieved data
    """
    user: str = None
    friends: list = None

class LfmUsers(object):
    """Gets a large number of last fm user names
    typical use would be ::
    lfmcrawler = LfmUsers(starting_user='musicfan')
    lfmcrawler.crawl(depth=2)"""
    def __init__(self, starting_user: str='oyo'):
        self.api_key = input("Last.fm Dev API Key")
        self.url = {'payload': {}, 'headers': {}}
        self.url['root'] = r'http://ws.audioscrobbler.com/2.0/'
        self.url['payload'] = {'method': 'user.getfriends', 'api_key': f'{self.api_key}',
                               'format': 'json', 'limit': 50, 'recenttracks': 'False'}
        self.url['headers']['user-agent'] = 'chrisoyer_my-app.0.0.1alpha'
        self.crawled = []
        self.userqueue = deque([starting_user])
        self.users = list()

    def _get_user_friends(self, user: str)->list:
        """requests data for one user and parses response"""
        payload = {**self.url['payload'], **{'user': user}}
        resp = requests.get(self.url['root'], params=payload, 
                            headers=self.url['headers']).json()
        return [friend['name'] for friend in resp['friends']['user']]
        
    def _process_userqueue(self):
        """runs through the queue"""
        users, self.userqueue = self.userqueue, []
        for user in users:
            friends = self._get_user_friends(user=user)
            user_and_friends = LfmUserData(user=user, friends=friends)
            self.users.append(user_and_friends)
            self.crawled.append(user)
            uncrawled_friends = [friend for friend in friends 
                                 if friend not in self.crawled]
            self.userqueue.extend(uncrawled_friends)
            sleep(randint(5,15))

    def crawl(self, friend_limit: Optional[int], depth: int=1)->None:
        """driver method. gets a large number of users
        parameters:    depth: loops through which to cycle; each time 
                              finding all connected users for already known users
        returns: None (adds to users attr and modifies userqueue attr)"""
        if friend_limit is not None:
            self.url['payload']['limit'] = friend_limit
        for layer in range(depth):
            self._process_userqueue()
            print(f"layer {layer} of {depth} done!")

    def to_json(self):
        """saves data to file in json format"""
        user_records = [asdict(user) for user in self.users]
        records_and_uncrawled = {'records': user_records,
                                 'uncrawled': self.userqueue}
        nowtime = datetime.now().strftime('%Y-%m-%dT%H%M%S')
        filename = f"../../../data/raw/unprocessed/lfm_users.{nowtime}.json"
        with open(filename, "w") as f:
            json.dump(records_and_uncrawled, f, indent=2)

    def to_db(self):
        """not implemented yet. Saves data directly to db
