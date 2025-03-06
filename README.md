# Whaller Client SDK in Python

## 📌 Introduction

This project is a Python SDK for interacting with the [Whaller API](https://developer.whaller.com/).

This library is in the early stages of implementation and contains only a few endpoints, but you can easily extend it by following the do. We encourage you to work with the Whaller teams on extending it.

## 📦 Installation

```sh
pip install whaller-client
```

## 🚀 Try the examples

### 1️⃣ **Set environment variables**

Before running examples scripts, you must create a `env.py` file with the following content as indicated in the `env.orig.py` file at the root of the examples folder:

```python
BASE_URL = "https://my.whaller.com"
CLIENT_ID = "your_client_id"
CLIENT_TOKEN = "your_client_token"
LOGIN = "your_email"
PASSWORD = "your_password"
```

> [!IMPORTANT]
> If you do not have client_id and client_token, please contact contact@whaller.com. Please note that there is a charge for obtaining these credentials.

### 2️⃣ **Run an authentication example**

An authentication example script is available in `examples/`. To run it:

```sh
cd examples/
python example_auth.py
```

If authentication is successful, you will see:

```sh
Authentication successful.
```

### 3️⃣ **Use the SDK in your project**

Minimal usage example:

```python
from whaller_client.client import Client
from whaller_client.endpoints.persons import Persons

# Initialize the client
client = Client(BASE_URL, CLIENT_ID, CLIENT_TOKEN)
client.set_credentials(LOGIN, PASSWORD)
client.authenticate()

# Example usage of endpoints
persons = Persons(client)
print(persons.get_notifications(LOGIN))
```

## 👨‍💻 For Developers

### Setting up the development environment

If you want to contribute to this project or modify it for your own needs, follow these steps to set up a development environment:

1. **Clone the repository**

```sh
git clone https://github.com/whallerfr/client-python.git
cd client-python
```

2. **Create a virtual environment (recommended)**

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the package in development mode**

```sh
pip install -e .
```

4. **Install development dependencies**

```sh
pip install pytest pytest-cov
```

### Running the tests

The project includes a comprehensive test suite with 100% code coverage. To run the tests:

```sh
python -m pytest
```

To run the tests with coverage report:

```sh
python -m pytest --cov=whaller_client
```

To generate an HTML coverage report:

```sh
python -m pytest --cov=whaller_client --cov-report=html
```

The HTML report will be available in the `htmlcov` directory. Open `htmlcov/index.html` in your browser to view it.

### Project structure

```
whaller_client/           # Main package
├── __init__.py           # Package initialization
├── api.py                # API client implementation
├── auth.py               # Authentication handling
├── client.py             # Main client class
├── exceptions.py         # Custom exceptions
├── logger.py             # Logging utilities
└── endpoints/            # API endpoints
    ├── __init__.py
    ├── box.py            # Box resource endpoints
    ├── invitation.py     # Invitation endpoints
    ├── me.py             # User-related endpoints
    └── upload.py         # File upload endpoints

tests/                    # Test suite
├── unit/                 # Unit tests
│   └── whaller_client/   # Tests for main package
│       ├── endpoints/    # Tests for endpoints
│       └── ...           # Tests for other modules
```

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## 📫 Support

For any questions or suggestions, open an issue on [GitHub](https://github.com/whallerfr/client-python/issues).

