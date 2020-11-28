from setuptools import setup, Distribution

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

    def has_ext_modules(foo):
        return True

setup(
    name="secrethub",
    version="0.0.2",
    author="SecretHub",
    description="Python client for the SecretHub Secrets Management API",
    url="https://secrethub.io",
    packages=['secrethub'],
    package_data={
        'secrethub': ['Client.dll', 'Client.so', '_secrethub.pyd', '_secrethub.so'],
    },
    distclass=BinaryDistribution,
    python_requires='>=3.9',
)
