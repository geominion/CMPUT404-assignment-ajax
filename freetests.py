#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# run python freetests.py

import urllib2
import unittest
import urlparse
import json
# your server
import server
import random

BASEHOST = '127.0.0.1'
BASEPORT = 5000

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        '''Check this out: we're not actually doing HTTP we're just calling the webservice directly'''
        self.app = server.app.test_client()

    def tearDown(self):
        '''nothing'''
        
    def testNothing(self):
        '''nothing'''

    def testHello(self):
        r = self.app.get('/')
        # a redirect is ok!
        self.assertTrue(r.status_code == 200 or
                        r.status_code == 301 or
                        r.status_code == 302
                        , "Code not 200!")
        if (r.status_code == 200):
            self.assertTrue(len(r.data) > 5, "No data?")

    def testUpdate(self):
        v = 'T'+str(random.randint(1,1000000))
        r = self.app.get(('/entity/%s' % v))
        self.assertTrue(r.status_code == 200, "Code not 200!")
        self.assertTrue(r.data == '{}', "Not empty? %s" % r.data)
        d = {'x':2, 'y':3}
        r = self.app.put(('/entity/%s' % v),data=json.dumps(d))
        self.assertTrue(r.status_code == 200, "PUT Code not 200!")
        rd = json.loads(r.data)
        for key in d:
            self.assertTrue(rd[key] == d[key], "KEY %s " % key)
        r = self.app.get(('/entity/%s' % v))
        self.assertTrue(r.status_code == 200, "Code not 200!")
        self.assertTrue(json.loads(r.data) == d, "D != r.data")

        
    def populateWorld(self):
        self.world = dict()
        for i in range(1,20):
            v = 'P'+str(random.randint(1,1000000))
            x = random.randint(1,640)
            y = random.randint(1,480)
            c = random.choice(['red','green','blue'])
            self.world[v] = {'x':x,'y':y,'colour':c}
        return self.world

    def testWorld(self):
        self.populateWorld()
        r = self.app.post('/clear')
        self.assertTrue(r.status_code == 200, "Code not 200!")
        for key in self.world:
            r = self.app.put(('/entity/%s' % key),
                             data=json.dumps(self.world[key]))
            self.assertTrue(r.status_code == 200, "Code not 200!")
            j = json.loads(r.data)
            self.assertTrue(len(j.keys()) >= 3,"JSON lacking keys! %s" % j.keys())
        r = self.app.get('/world')
        self.assertTrue(r.status_code == 200, "Code not 200!")
        newworld = json.loads(r.data)
        for key in self.world:
            self.assertTrue(self.world[key]  == newworld[key], "Key %s" % key)


        
        
        

if __name__ == '__main__':
    unittest.main()
