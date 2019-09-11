from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='monitoria',
    version='1.0',
    description='Module to help with the PA job',
    author='Ariel Yssou',
    long_description=long_description,
    author_email='arielyssou@gmail.com',
    install_requires=['faker', 'curses'], #external packages as dependencies
)
