# -*- coding: utf-8 -*-
#
from setuptools import setup, find_packages
import os
import codecs

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, 'code_extract', '__about__.py'), 'rb') as f:
    exec(f.read(), about)


def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
            ).read()
    except Exception:
        content = ''
    return content


setup(
    name='code_extract',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(),
    description=(
       'Extract code blocks from text files'
       ),
    long_description=read('README.rst'),
    url='https://github.com/nschloe/code_extract',
    download_url='https://github.com/nschloe/code_extract/releases',
    license=about['__license__'],
    platforms='any',
    install_requires=[
        ],
    classifiers=[
        about['__status__'],
        about['__license__'],
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing'
        ],
    scripts=[
        'tools/code-extract'
        ]
    )
