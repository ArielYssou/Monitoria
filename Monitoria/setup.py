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
    #packages=['modules'],  #same as name
    install_requires=['faker', 'random', 'curses', 'datetime', 'shutil'], #external packages as dependencies
    #data_files=[('./files', []), ('./grades', []),('./grades/*', []) ]
)
