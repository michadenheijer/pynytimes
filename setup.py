import setuptools

from pynytimes import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynytimes",
    version=__version__,
    description="A Python wrapper for (most) New York Times APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Micha den Heijer",
    author_email="micha@michadenheijer.com",
    python_requires="~=3.5",
    packages=setuptools.find_packages(),
    include_package_data = True,
    url="https://github.com/michadenheijer/pynytimes",
    license="MIT",
    install_requires = ["requests==2.23.0"],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
    ]
)