#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from whaller_client.client import Client

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from examples.env import BASE_URL, CLIENT_ID, CLIENT_TOKEN, LOGIN, PASSWORD

# Client initialization
client = Client(BASE_URL, CLIENT_ID, CLIENT_TOKEN)

# Authentication
try:
    client.set_credentials(LOGIN, PASSWORD)
    client.authenticate()
    print("Authentication successful.")
except Exception as e:
    print(f"Authentication failed: {e}")
