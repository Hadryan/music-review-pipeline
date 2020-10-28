#!/usr/bin/python/
import requests
import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from collections import deque
from time import sleep

@dataclass_json
@dataclass
class LfmUserData():
    """dataclass to store retrieved data
    typical use would be ::
        lfmcrawler = LfmUsers()
        lfmcrawler.crawl(starting_user='musicfan', depth=2)"""
    user: str = None
    friends: list = None

class LfmUsers(object):
    """Gets a large number of last fm user names"""
    def __init__(self, starting_user: str='oyo'):
        self.api_key = input("Last.fm Dev API Key")
        self.url = {'payload': {}, 'headers': {}}
        self.url['root'] = r'http://ws.audioscrobbler.com/2.0/'
        self.url['payload']['method'] = 'user.getfriends'
        self.url['payload']['api_key'] = f'{self.api_key}'
        self.url['payload']['format'] = 'json'
        self.url['payload']['recenttracks'] = 'False'
        self.url['headers']['user-agent'] = 'chrisoyer_my-app.0.0.1alpha'
        self.crawled = []
        self.userqueue = deque([starting_user])
        self.users = [starting_user]

    def _get_user_friends(self, user, friend_limit: int=50):
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
            sleep(5)

    def crawl(self, depth: int=1):
        """driver method. gets a large number of users
        parameters:    depth: loops through which to cycle; each time 
                              finding all connected users for already known users
        returns: None (adds to users attr and modifies userqueue attr)"""

        for layer in range(depth):
            self._process_userqueue()
            print(f"layer {layer} of {depth} done!")
    def to_json(self, filename:str="../../../data/raw/lfm_users.json"):
        """saves data to file in json format"""
        json_object = json.dumps(self.users.to_json(), indent = 4) 
  
        with open(filename, "w") as outfile: 
            outfile.write(json_object) 
