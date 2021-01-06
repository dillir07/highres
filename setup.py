import os
import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name='highres',
    version='1.0.1',
    author="Dilli Babu R",
    author_email="dillir07@outlook.com",
    description='A script to download hi-resolution images using google search by image feature',
    long_description=read('pip-readme.rst'),
    long_description_contect_type="text/markdown",
    url="https://dillir07.github.io/hires/",
    packages=['hiresmodule'],
    install_requires=['selenium'],
    entry_points={
        "console_scripts": ['hires=hiresmodule.command_line:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
