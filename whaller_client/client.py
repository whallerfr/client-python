import logging
from whaller_client.auth import Authenticator
from whaller_client.api import ApiClient
from whaller_client.logger import Logger

class Client:
    def __init__(self, base_url:str, client_id:str, client_token:str) -> None:
        self.authenticator = Authenticator(client_id, client_token)
        self.api = ApiClient(base_url)
        self.logger = Logger('api', level=logging.INFO)

    def set_credentials(self, login:str, password:str) -> None:
        self.authenticator.set_credentials(login, password)

    def authenticate(self):
        self.authenticator.authenticate(self.api)
    
    def get_api_token(self):
        return self.authenticator.get_bearer_token()

    def call_post(self, endpoint:str, data:dict={}, with_auth:bool=False) -> dict:
        headers = {}
        if with_auth:
            headers.update(self.get_api_token())
        return self.api.call_json(endpoint, "POST", data, headers)
    
    def call_get(self, endpoint:str, data:dict={}, with_auth:bool=False) -> dict:
        headers = {}
        if with_auth:
            headers.update(self.get_api_token())
        return self.api.call_json(endpoint, "GET", data, headers)
