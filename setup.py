from setuptools import setup, Extension
from sys import platform

extension=''
if platform == "linux" or platform == "linux2":
    extension = '.so'
elif platform == "darwin":
    extension = '.dylib'
elif platform == "win32":
    extension = '.lib'

setup(
    name="secrethub",
    version="0.0.7",
    author="SecretHub",
    description="Python client for the SecretHub Secrets Management API",
    url="https://secrethub.io",
    ext_modules=[Extension('_secrethub', ['secrethub.i'], extra_objects=['Client'+extension])],
    py_modules=['secrethub'],
    python_requires='>=3.8',
)
