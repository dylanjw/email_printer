#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='faxta',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='0.0.0-alpha.0',
    description="""Faxta, email your printer.""",
    long_description_markdown_filename='README.md',
    author='Dylan Wilson',
    author_email='dylanjw@protonmail.com',
    url='https://github.com/dylanjw/email_printer',
    include_package_data=True,
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest',
            'hypothesis',
        ]
    },
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.6,<4',
    py_modules=['faxta', 'golemail', 'faxta_utils'],
    license="GPL-3.0",
    zip_safe=False,
    keywords='python',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
