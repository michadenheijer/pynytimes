import setuptools
import os

location = os.path.abspath(os.path.dirname(__file__))

about_module = {}
with open(
    os.path.join(location, "pynytimes", "__version__.py"),
    mode="r",
    encoding="utf-8",
) as f:
    exec(f.read(), about_module)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynytimes",
    version=about_module["__version__"],
    description=about_module["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=about_module["__author__"],
    author_email=about_module["__author_email__"],
    python_requires=">=3.9, <4",
    packages=setuptools.find_packages(),
    include_package_data=True,
    url=about_module["__url__"],
    license=about_module["__license__"],
    install_requires=["requests>=2.10.0,<3.0.0", "urllib3>=2.0.0"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Sociology",
    ],
)
