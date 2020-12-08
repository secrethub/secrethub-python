from setuptools import setup, Extension
from sys import platform

extra_obj_extension=''
package_data = {}
if platform == "linux" or platform == "linux2":
    extra_obj_extension = '.so'
elif platform == "darwin":
    extra_obj_extension = '.dylib'
elif platform == "win32":
    extra_obj_extension = '.lib'
    package_data = {
        'secrethub': ['Client.dll'],
    }

setup(
    name="secrethub",
    version="0.0.7",
    author="SecretHub",
    description="Python client for the SecretHub Secrets Management API",
    url="https://secrethub.io",
    ext_modules=[Extension('_secrethub', ['secrethub.i'], extra_objects=['Client'+extra_obj_extension])],
    py_modules=['secrethub'],
    package_data=package_data,
    python_requires='>=3.8',
)
