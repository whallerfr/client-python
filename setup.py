from setuptools import setup, find_packages

setup(
    name="whaller-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    author="Whaller",
    author_email="contact@whaller.com",
    description="Python SDK for interacting with the Whaller API",
    url="https://github.com/whallerfr/client-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
