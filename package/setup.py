from setuptools import setup, find_packages, Extension, Distribution
from setuptools.command.build_ext import build_ext
import os
import pathlib
import shutil

suffix = '.pyd' if os.name == 'nt' else '.so'

class CustomDistribution(Distribution):
  def iter_distribution_names(self):
    for pkg in self.packages or ():
      yield pkg
    for module in self.py_modules or ():
      yield module

class CustomExtension(Extension):
  def __init__(self, path):
    self.path = path
    super().__init__(pathlib.PurePath(path).name, [])

class build_CustomExtensions(build_ext):
  def run(self):
    for ext in (x for x in self.extensions if isinstance(x, CustomExtension)):
      source = f"{ext.path}{suffix}"
      build_dir = pathlib.PurePath(self.get_ext_fullpath(ext.name)).parent
      os.makedirs(f"{build_dir}/{pathlib.PurePath(ext.path).parent}",
          exist_ok = True)
      shutil.copy(f"{source}", f"{build_dir}/{source}")

def find_extensions(directory):
  extensions = []
  for path, _, filenames in os.walk(directory):
    for filename in filenames:
      filename = pathlib.PurePath(filename)
      if pathlib.PurePath(filename).suffix == suffix:
        extensions.append(CustomExtension(os.path.join(path, filename.stem)))
  return extensions

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
    distclass=CustomDistribution,
    ext_modules = find_extensions("PackageRoot"),
    cmdclass = {'build_ext': build_CustomExtensions},
    python_requires='>=3.9',
)
