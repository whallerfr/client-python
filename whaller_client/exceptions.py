class MethodError(Exception):
    """ Exception raised for an invalid HTTP method. """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class ApiError(Exception):
    """ Exception raised when the API returns an error message. """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class HttpError(Exception):
    """ Exception raised for an HTTP request issue (e.g., timeout, 404, 500, etc.). """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class InvalidResponseError(Exception):
    """ Exception raised if the JSON response is malformed. """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class UploadError(Exception):
    """ Exception raised for an error during file upload. """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
