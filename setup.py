import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynytimes",
    version="0.1-alpha",
    description="A Python wrapper for (most) New York Times APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Micha den Heijer",
    author_email="micha@michadenheijer.com",
    python_requires="~=3.4",
    packages=setuptools.find_packages(exclude("tests",)),
    license="MIT",
    install_requires = [
        "requests==2.22.0"
    ]
)