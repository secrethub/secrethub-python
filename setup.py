from setuptools import setup, Extension, Distribution
from sys import platform
from codecs import open

extra_obj_extension=''
if platform == "linux" or platform == "linux2":
    extra_obj_extension = '.so'
elif platform == "darwin":
    extra_obj_extension = '.dylib'
elif platform == "win32":
    extra_obj_extension = '.lib'

readme = open('README.md', 'r')
readme_contents = readme.read()
readme.close()

setup(
    name="secrethub",
    version="0.1.0",
    author="SecretHub",
    author_email="support@secrethub.io",
    license="Apache License Version 2.0",
    keywords="secrets management api devops",
    description="Python client for the SecretHub Secrets Management API",
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    url="https://secrethub.io/",
    ext_modules=[Extension('secrethub._secrethub', ['secrethub/secrethub.i'], extra_objects=['secrethub/Client'+extra_obj_extension])],
    packages=['secrethub'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        'Bug Reports': 'https://github.com/secrethub/secrethub-python/issues',
        'Source': 'https://github.com/secrethub/secrethub-python/',
    },
)
