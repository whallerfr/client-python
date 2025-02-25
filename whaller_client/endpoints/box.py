import os
from whaller_client.client import Client
from whaller_client.endpoints.upload import Upload

class Box:
    def __init__(self, client: Client, external_id: str) -> None:
        """
        Class to manage file and folder storage within an organization.
        """
        self.client = client
        self.sphere_external_id = external_id
        self.upload_client = Upload(client)

    def create_folder(self, name: str, parent_id: int | None = None) -> int:
        """
        Creates a folder within the organization.

        :param name: Name of the folder
        :param parent_id: ID of the parent folder (optional)
        :return: ID of the created folder
        """
        data = {
            'name': name,
            'type': 1
        }
        if parent_id is not None:
            data['parent_id'] = parent_id

        response = self.client.call_auth_post(f'spheres/{self.sphere_external_id}/boxresources', data)
        return response.get('id', -1)  # Returns -1 if 'id' is not in the response

    def create_file(self, name: str, content: bytes, mimes: str, parent_id: int | None = None) -> dict:
        """
        Uploads a file and creates an associated resource.

        :param name: Name of the file
        :param content: Content of the file as bytes
        :param mimes: MIME type of the file
        :param parent_id: ID of the parent folder (optional)
        :return: Dictionary containing the information of the created file
        """
        file_data = self.upload_client.boxresource(name, content, mimes, self.sphere_external_id)

        resource = {
            'name': os.path.splitext(name)[0],  # Name without extension
            'ext': os.path.splitext(name)[1].lstrip('.'),  # Extension without the dot
            'cloudfile_id': file_data['id'],
            'type': 2
        }

        if parent_id is not None:
            resource['parent_id'] = parent_id

        return self.client.call_auth_post(f'spheres/{self.sphere_external_id}/boxresources', resource)
