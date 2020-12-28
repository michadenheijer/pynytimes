import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynytimes",
    version="0.4.2",
    description="A Python wrapper for (most) New York Times APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Micha den Heijer",
    author_email="micha@michadenheijer.com",
    python_requires=">=3.5, <3.10",
    packages=setuptools.find_packages(),
    include_package_data = True,
    url="https://github.com/michadenheijer/pynytimes",
    license="MIT",
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
