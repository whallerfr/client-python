from whaller_client.client import Client

class Me:
    def __init__(self, client: Client):
        """
        Initializes the Persons class with a client.

        :param client: Instance of the Client class
        """
        self.client = client

    def get_notifications(self, login: str):
        """
        Retrieves notifications for a given user.

        :param login: User's login identifier
        :return: User's notifications
        :link: https://developer.whaller.com/#api-Me-persons
        """
        return self.client.call_get(f"persons/{login}/notifications", {}, True)
    
    def list_spheres(self):
        """
        Retrieves a list of spheres for the current user.

        :return: List of spheres
        :link: https://developer.whaller.com/#api-Me-spheres
        """
        return self.client.call_get("me/spheres", {}, True)