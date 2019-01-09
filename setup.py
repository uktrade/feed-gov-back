import os
from setuptools import find_packages, setup
from feedback import __version__, __author__, __email__


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='feed-gov-back',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A small framework for API enabled customisable feedback forms',
    long_description=README,
    url='https://github.com/uktrade/feed-gov-back',
    author=__author__,
    author_email=__email__,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'psycopg2-binary',
        'Django',
        'djangorestframework',
    ]
)
