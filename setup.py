from setuptools import setup

setup(
    name = "Kay_ugit",
    version = "0.0.1",
    packages = ["ugit"],
    entry_points = {
        "console_scripts" : ["ugit = ugit.cli:main"]
    }
)