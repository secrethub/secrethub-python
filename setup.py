from setuptools import setup, Extension, Distribution
from sys import platform

extra_obj_extension=''
if platform == "linux" or platform == "linux2":
    extra_obj_extension = '.so'
elif platform == "darwin":
    extra_obj_extension = '.dylib'
elif platform == "win32":
    extra_obj_extension = '.lib'

setup(
    name="secrethub",
    version="0.0.7",
    author="SecretHub",
    description="Python client for the SecretHub Secrets Management API",
    url="https://secrethub.io",
    ext_modules=[Extension('_secrethub', ['secrethub.i'], extra_objects=['Client'+extra_obj_extension])],
    py_modules=['secrethub'],
    python_requires='>=3.8',
)
