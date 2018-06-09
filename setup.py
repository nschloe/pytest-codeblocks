# -*- coding: utf-8 -*-
#
from setuptools import setup, find_packages
import os
import codecs

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "excode", "__about__.py"), "rb") as f:
    exec(f.read(), about)


def read(fname):
    return codecs.open(os.path.join(base_dir, fname), encoding="utf-8").read()


setup(
    name="excode",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    packages=find_packages(),
    description=("Extract code blocks from text files"),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/nschloe/excode",
    license=about["__license__"],
    platforms="any",
    install_requires=[],
    classifiers=[
        about["__status__"],
        about["__license__"],
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing",
    ],
    scripts=["tools/excode"],
)
