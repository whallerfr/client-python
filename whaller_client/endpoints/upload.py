import uuid
import math
from whaller_client.client import Client

class Upload:
    def __init__(self, client: Client) -> None:
        """
        Class that manages the upload of a document within an organization.
        """
        self.client = client
        self.chunksize = 10 * 1024 * 1024  # 10 MB

    def _upload(self, endpoint: str, params: dict, files: dict) -> dict:
        """
        Performs a standard file upload.
        """
        return self.client.send_post_content(endpoint, params, files)

    def _upload_with_chunking(self, endpoint: str, filename: str, content: bytes, mimes: str, sphere_external_id: str = None) -> dict:
        """
        Performs a chunked upload for large files.

        :param endpoint: API endpoint for the upload
        :param filename: Name of the file
        :param content: File content in bytes
        :param mimes: MIME type of the file
        :param sphere_external_id: External ID of the sphere (optional)
        :return: API response after upload
        """
        dzuuid = uuid.uuid4()
        dztotalfilesize = len(content)
        dztotalchunkcount = math.ceil(dztotalfilesize / self.chunksize)

        for dzchunkindex in range(dztotalchunkcount):
            start = dzchunkindex * self.chunksize
            end = min(start + self.chunksize, dztotalfilesize)
            dzcontent = content[start:end]
            dzchunkbyteoffset = start
            dzchunksize = len(dzcontent)
            files = {'userfile': (filename, dzcontent, mimes)}

            params = {
                'dzuuid': str(dzuuid),
                'dztotalfilesize': dztotalfilesize,
                'dztotalchunkcount': dztotalchunkcount,
                'dzchunkindex': dzchunkindex,
                'dzchunkbyteoffset': dzchunkbyteoffset,
                'dzchunksize': dzchunksize,
            }

            if sphere_external_id:
                params['sphere_id'] = sphere_external_id

            response = self._upload(endpoint, params, files)

        return response

    def boxresource(self, filename: str, content: bytes, mimes: str, sphere_external_id: str) -> dict:
        """
        Uploads a file and creates an associated resource.

        :param filename: Name of the file
        :param content: File content in bytes
        :param mimes: MIME type of the file
        :param sphere_external_id: Sphere ID
        :return: API response after upload
        """
        endpoint = 'upload/box_resource'

        if len(content) > self.chunksize:
            return self._upload_with_chunking(endpoint, filename, content, mimes, sphere_external_id)

        params = {'sphere_id': sphere_external_id}
        files = {'userfile': (filename, content, mimes)}

        return self._upload(endpoint, params, files)
