from setuptools import setup, Extension

setup(
    name="secrethub",
    version="0.0.7",
    author="SecretHub",
    description="Python client for the SecretHub Secrets Management API",
    url="https://secrethub.io",
    ext_modules=[Extension('_secrethub', ['secrethub.i'], extra_objects=['Client.so'])],
    py_modules=['secrethub'],
    python_requires='>=3.8',
)
