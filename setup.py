#!usr/bin/env python

from setuptools import setup, find_packages
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'diffbot'))

from diffbot.version import VERSION

setup(
    name="diffbot",
    version=VERSION,
    description="The diffbot package provides functions to interact with the Diffbot API.",
    author="Christian Hubbs",
    license="MIT",
    url="https://github.com/hubbs5/diffbot",
    packages=find_packages(),
    # TODO: update required packages
    install_requires=[
        "requests>=2.0",
        "pandas>=1.0",
        "numpy>=1.0",
    ],
    python_requires=">=3.5",
    classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	]
)