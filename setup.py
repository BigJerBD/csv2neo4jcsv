from distutils.core import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='csv2neo4jcsv',
    version='0.1',
    description='Util to convert a csv to a neo4j csv',
    author='Jeremie Bigras-Dunberry',
    author_email='Bigjerbd@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url='https://github.com/BigJerBD/csv2neo4jcsv',
    license='MIT License',
    platforms=['POSIX', 'Windows', 'Unix', 'MacOS'],
    keywords=['python', 'csv','Neo4j'],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ),
)
