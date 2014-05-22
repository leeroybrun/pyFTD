from setuptools import setup, find_packages
setup(
    name = "pyFTD",
    version = "0.1",
    packages = find_packages(),

    install_requires = ['pyv8', 'requests'],

    # metadata for upload to PyPI
    author = "Leeroy Brun",
    author_email = "leeroy.brun@gmail.com",
    description = "FrenchTorrentDB python example",
    license = "MIT",
    keywords = "torrents frenchtorrentdb ftd",
    url = "https://github.com/leeroybrun/pyFTD", 
)