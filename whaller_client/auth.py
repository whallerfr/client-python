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

    def get_bearer_token(self, api_client: ApiClient):
        if self.token is None:
            self.authenticate(api_client)
        return {"Authorization": "Bearer " + self.token}

    def refresh_token(self, api_client: ApiClient):
        """
        Refresh the token before it expires.
        """
        if self.token is None:
            self.authenticate(api_client)
        data = {'auth_token': self.token, 'login': self.login, 'renew': True}
        response = api_client.call_json('person/status_auth_by_token', 'POST', data, self.get_bearer_token(api_client))
        self.token = response['auth_token']
