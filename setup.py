from distutiles.core import setup

setup(
    name="pynytimes",
    version="0.1-alpha",
    description="A Python wrapper for (most) New York Times APIs",
    author="Micha den Heijer",
    author_email="micha@michadenheijer.com",
    python_requires="~=3.4",
    packages=["requests",],
    license="MIT"
)