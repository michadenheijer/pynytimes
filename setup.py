import setuptools
import os

location = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(location, 'pynytimes', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = about["__title__"],
    version = about["__version__"],
    description = about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = about["__author__"],
    author_email = about["__author_email__"],
    python_requires = ">=3.5, <3.10",
    packages = setuptools.find_packages(),
    include_package_data = True,
    url = about["__url__"],
    license = about["__license__"],
    install_requires = ["requests==2.25.1"],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Sociology"
    ]
)
