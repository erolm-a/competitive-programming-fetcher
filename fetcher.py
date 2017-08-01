#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Simple fetcher for many CP sites

import json
import requests
import random

# OIS tasks are excluded
def fetch_OII():
    payload = {'first': 0, 'last': 0, 'action': 'list'}
    url = 'https://cms.di.unipi.it/api/task'
    r = requests.post(url, json=payload)
    if r.status_code is not 200:
        print("Unable to fetch the tasks: {}".format(r.reason()))
    else:
        length = int(r.json()['num'])
        payload['last'] = length
        r = requests.post(url, json=payload)
        task_list = [x['name'] for x in r.json()['tasks']]
        tasks = sorted(filter(lambda s: not s.startswith('ois'), task_list))
        return "https://cms.di.unipi.it/#/task/{}/statement".format(random.choice(tasks))
