
from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = "django-scenic",
    version = "0.1.0",
    description = "Collaboration based views for Django",
    author = "Michael Jones",
    author_email = "m.pricejones@gmail.com",
    url = "",
    packages = find_packages(),
    include_package_data=True,
    install_requires = ['django'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules ',
    ],
)
