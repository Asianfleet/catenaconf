# -*- coding: utf-8 -*-
import io
from setuptools import setup, find_packages

# 读取README.md文件
with io.open("README-pkg.md", encoding="utf-8") as f:
    long_description = f.read()
    
# 读取requirements.txt文件
with open("requirements.txt") as f:
    required = f.read().splitlines()
    
setup(
    name="catenaconf",
    version="0.1.3",
    packages=find_packages(),
    install_requires=required,
    description="A python configuration management library based on dict, with similar grammar as omegaconf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jianqing Wang",
    author_email="18353419066@163.com",
    url="https://github.com/Asianfleet/catenaconf",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
