from setuptools import setup, Extension
from sys import platform

extra_obj_extension=''
shared_obj_extension=''
if platform == "linux" or platform == "linux2":
    extra_obj_extension = '.so'
    shared_obj_extension = '.so'
elif platform == "darwin":
    extra_obj_extension = '.dylib'
    shared_obj_extension = '.dylib'
elif platform == "win32":
    extra_obj_extension = '.lib'
    shared_obj_extension = '.dll'

setup(
    name="secrethub",
    version="0.0.7",
    author="SecretHub",
    description="Python client for the SecretHub Secrets Management API",
    url="https://secrethub.io",
    ext_modules=[Extension('_secrethub', ['secrethub.i'], extra_objects=['Client'+extension])],
    py_modules=['secrethub'],
    libraries=['Client'+shared_obj_extension]
    python_requires='>=3.8',
)
