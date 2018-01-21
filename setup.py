#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="python-enotas-emissor",
      version="1.0.0",
      description="eNotas Emissor python",
      license="MIT",
      install_requires=["simplejson","httplib2","six"],
      author="Thales",
      author_email="tsf.2007@gmail.com",
      url="https://github.com/thales91",
      packages = find_packages(),
      keywords= "enotas-emissor",
      zip_safe = True)
