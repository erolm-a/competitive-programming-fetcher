#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright by Enrico "erolm_a" Trombetta
#
# This file is part of Competitive Programming Fetcher
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

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
