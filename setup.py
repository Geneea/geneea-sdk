# coding=utf-8

"""
Set up packaging, unit tests and dependencies.
"""

from setuptools import setup, find_packages

setup(
    name="geneeasdk",
    version="0.1",

    author="Geneea Analytics",
    author_email="support@geneea.com",
    description="SDK for the Interpretor API",
    keywords="Geneea Interpretor integration SDK",
    url="http://geneea.com",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Supported Python versions
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # Dependencies
    install_requires = ['requests>=2.9.0', 'PyYAML>=3.10', 'junit_xml>=1.7'],

    packages=find_packages(include=['geneeasdk', 'geneeasdk.*']),

    # setup will create executable scripts based on this list
    entry_points={
        'console_scripts': [

        ],
    },

    test_suite="tests"
)
