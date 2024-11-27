import setuptools
from setuptools import setup, find_packages

setup(
    name="valentinas-p_mod1-atsiskaitymas",
    version = "0.1",
    author = "Valentinas Popov",
    description = "",
    packages= setuptools.find_packages(where="."),
    install_requires = [
        'requests == 2.32.3',
        'lxml >= 5.3.0',
    ],
    python_requires = ">=3.10"
)