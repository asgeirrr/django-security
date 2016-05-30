#!/usr/bin/env python
# -*- coding: utf-8 -*-
from security.version import get_version

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-security',
    version=get_version(),
    description="Django security library.",
    keywords='django, throttling',
    author='Lubos Matl',
    author_email='matllubos@gmail.com',
    url='https://github.com/matllubos/django-security',
    license='LGPL',
    package_dir={'security': 'security'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 0 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU LESSER GENERAL PUBLIC LICENSE (LGPL)',
        'Natural Language :: Czech',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=[
        'django>=1.6',
        'django-jsonfield>=0.9.19',
        'django-json-field==0.5.8',
        'django-ipware>=1.0.0',
        'django-chamber>=0.1.9',
    ],
    dependency_links=[
        'https://github.com/matllubos/django-json-field/tarball/0.5.8#egg=django-json-field-0.5.8',
        'https://github.com/matllubos/django-chamber/tarball/0.1.9#egg=django-chamber-0.1.9',
    ],
    zip_safe=False
)
