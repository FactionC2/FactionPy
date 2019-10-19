import os
import sys
from setuptools import setup, find_packages


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="factionpy",
    version="0.0.1",
    author="The Faction Team",
    author_email="team@factionc2.com",
    description="Common Library for Python based Faction services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FactionC2/factionpy",
    packages=find_packages(),
    classifiers=[],
    python_requires='>=3.6',
)
