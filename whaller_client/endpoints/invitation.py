from whaller_client.client import Client

class Invitation:
    def __init__(self, client: Client) -> None:
        self.client = client

    def remove_one(self, invitation_id: int) -> None:
        data = {"id": invitation_id}
        self.client.call_auth_post('invitation', data=data)