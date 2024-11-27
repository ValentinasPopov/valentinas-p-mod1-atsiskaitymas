import setuptools
from setuptools import setup, find_packages

setup(
    name="valentinas-p_mod1-atsiskaitymas",
    version = "0.12",
    author = "Valentinas Popov",
    description = "",
    packages= setuptools.find_packages(where="."),
    install_requires = [
        'requests == 2.32.3',
        'lxml >= 5.3.0',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires = ">=3.10",
    url = "https://github.com/ValentinasPopov/valentinas-p-mod1-atsiskaitymas/tree/master/valentinas_p_mod1_atsiskaitymas"
)