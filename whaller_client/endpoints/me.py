from whaller_client.client import Client

class Me:
    def __init__(self, client: Client):
        """
        Initializes the Persons class with a client.

        :param client: Instance of the Client class
        """
        self.client = client

    def get(self):
        """
        Retrieves the current user's information.

        :return: Current user's information
        :link: https://developer.whaller.com/#api-Me
        """
        return self.client.call_get("me", {}, True)
    
    def get_notifications(self, login: str):
        """
        Retrieves notifications for a given user.

        :param login: User's login identifier
        :return: User's notifications
        :link: https://developer.whaller.com/#api-Me-persons
        """
        return self.client.call_get(f"persons/{login}/notifications", {}, True)
    
    def list_spheres(self, data: dict = {}):
        """
        Retrieves a list of spheres for the current user.

        :return: List of spheres
        :link: https://developer.whaller.com/#api-Me-spheres
        """
        return self.client.call_get("me/spheres", data, True)
    
    def list_networks(self, data: dict = {}):
        """
        Retrieves a list of organizations and spheres for the current user.

        :return: List of organizations and spheres
        :link: https://developer.whaller.com/#api-Me-network
        """
        return self.client.call_get("me/networks", data, True)
    
    def list_phones(self, status: str = ""):
        """
        Retrieves a list of phones for the current user.

        :param status: Status of the phones to retrieve (optional)

        :return: List of phones
        :link: https://developer.whaller.com/#api-Me-MyPhoneNumbers
        """
        if status:
            data = {"status": status}
        else:
            data = {}
        return self.client.call_get("me/phones", data, True)
    