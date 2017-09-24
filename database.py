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

# Database class

import sqlite3
import conf
from asyncio import Lock

class Database:
    def __init__(self):
        self._db = sqlite3.connect(conf.LOCAL_DB, check_same_thread=False)
        self._c = self._db.cursor()
        self._c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER NOT NULL PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''');
        self._db.commit()
    
    def __del__(self):
        self.flush()
        self._db.close()
    
    def register_chat_id(self, chat_id):
        # If the element already exists, just ignore it
        self._c.execute('INSERT OR IGNORE INTO users ("chat_id") VALUES(?)', (chat_id,))

    def get_chat_list(self):
        # what kind of error could this line raise?
        return self._c.execute('SELECT chat_id FROM users')

    def flush(self):
        # what kind of error could this line raise?
        self._db.commit()
        

