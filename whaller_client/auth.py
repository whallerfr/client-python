from base64 import b64encode
from whaller_client.api import ApiClient

class Authenticator:
    def __init__(self, client_id: str, client_token: str):
        self.client_id = client_id
        self.client_token = client_token
        self.token = None
        self.login = None
        self.password = None

    def set_credentials(self, login: str, password: str):
        self.login = login
        self.password = password

    def authenticate(self, api_client: ApiClient):
        token = (self.client_id + ':::' + self.client_token).encode("utf-8")
        header_application = {"X-Application": b64encode(token)}
        data = {'signin-login': self.login, 'signin-password': self.password}

        response = api_client.call_json('person/login', 'POST', data, header_application)
        self.token = response['auth_token']

    def get_bearer_token(self):
        if self.token is None:
            self.authenticate()
        return {"Authorization": "Bearer " + self.token}
