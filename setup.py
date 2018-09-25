#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='figureAltCaption',
    version='1.0.0',
    description='Extension for Python-Markdown to parse images with captions.',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/jdittrich/figureAltCaption',
    py_modules=['figureAltCaption'],
    install_requires=['Markdown>=2.0,<3.0', ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities'
    ]
)
