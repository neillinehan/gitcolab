
from setuptools import setup, find_packages

setup(
        name='gitcolab',
        version='0.1',
        packages=find_packages(),
        install_requires=['gitpython'],
        author='neillinehan',
        author_email='neiledwardlinehan@gmail.com',
        description='A user-friendly package to automate the process of creating and pushing a Python package to GitHub.',
        url='https://github.com/neillinehan/gitcolab',
)
