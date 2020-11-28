import setuptools

class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True

setuptools.setup(
    name="secrethub",
    version="0.0.1",
    author="SecretHub",
    description="Python client for the SecretHub Secrets Management API",
    url="https://secrethub.io",
    packages=['secrethub'],
    package_data={
        'secrethub': ['Client.dll', '_secrethub.pyd'],
    },
    distclass=BinaryDistribution,
    python_requires='>=3.9',
)
