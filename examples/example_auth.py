#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, script_dir)

from whaller_client.client import Client

try:
    from examples.env import BASE_URL, CLIENT_ID, CLIENT_TOKEN, LOGIN, PASSWORD
except ModuleNotFoundError:
    from env import BASE_URL, CLIENT_ID, CLIENT_TOKEN, LOGIN, PASSWORD

# Client initialization
client = Client(BASE_URL, CLIENT_ID, CLIENT_TOKEN)

# Authentication
try:
    client.set_credentials(LOGIN, PASSWORD)
    client.authenticate()
    print("Authentication successful. Token: " + client.get_api_token()['Authorization'])
    time.sleep(1)
    client.refresh_token()
    print("Token refreshed. Token: " + client.get_api_token()['Authorization'])
except Exception as e:
    print(f"Authentication failed: {e}")
