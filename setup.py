import os
import sys
import shutil
from setuptools import setup, find_packages
from factionpy import VERSION

def clean():
    if os.path.exists("./build"):
        shutil.rmtree('./build')
    if os.path.exists("./dist"):
        shutil.rmtree('./dist')
    if os.path.exists("./factionpy.egg-info"):
        shutil.rmtree('./factionpy.egg-info')


if sys.argv[-1] == 'clean':
    clean()

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    clean()
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    clean()
    sys.exit()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="factionpy",
    version=VERSION,
    author="The Faction Team",
    author_email="team@factionc2.com",
    description="Common Library for Python based Faction applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FactionC2/factionpy",
    packages=find_packages(),
    license="MIT",
    classifiers=[],
    python_requires='>=3.8',
    install_requires=['bcrypt', 'pyjwt', 'kubernetes', 'gql', 'httpx', 'pydantic', 'python-dateutil'],
    extras_require={
        'fastapi': ["fastapi"]
    }
)
