#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from whaller_client.client import Client
from whaller_client.endpoints.me import Me

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from examples.env import BASE_URL, CLIENT_ID, CLIENT_TOKEN, LOGIN, PASSWORD

# Client initialization
client = Client(BASE_URL, CLIENT_ID, CLIENT_TOKEN)

# Authentication
client.set_credentials(LOGIN, PASSWORD)
client.authenticate()

me = Me(client)
print(me.get_notifications(LOGIN))

print(me.list_spheres())