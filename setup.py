from setuptools import setup, find_packages

setup(
    name='catenaconf',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        # 如果有其他依赖项，可以在这里列出
    ],
    description='A configuration management library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jianqing Wang',
    author_email='1239326528@qq.com',
    url='https://github.com/yourusername/catenaconf',  # 如果有的话
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
