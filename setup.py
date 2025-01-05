# -*- coding: utf-8 -*-
import io
from setuptools import setup, find_packages

with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='catenaconf',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    description='A configuration management library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jianqing Wang',
    author_email='18353419066@163.com',
    url='https://github.com/Asianfleet/catenaconf',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
