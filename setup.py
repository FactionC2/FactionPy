import os
import sys
from setuptools import setup, find_packages
from factionpy import VERSION


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    if os.path.exists("./build"):
        os.system('rm -f ./build')
    if os.path.exists("./dist"):
        os.system('rm -f ./dist')
    if os.path.exists("./factionpy.egg-info"):
        os.system('rm -f ./factionpy.egg-info')
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="factionpy",
    version=VERSION,
    author="The Faction Team",
    author_email="team@factionc2.com",
    description="Common Library for Python based Faction services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FactionC2/factionpy",
    packages=find_packages(),
    license="MIT",
    classifiers=[],
    python_requires='>=3.6', install_requires=['bcrypt', 'bcrypt', 'bcrypt']
)
