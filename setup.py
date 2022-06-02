from setuptools import setup, find_packages

setup(
    name="twoker",
    version="0.1.0",
    description="twitter crawling tool",
    author="shuyaeer",
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        "console_scripts": [
            "twoker=twitter_collector.cli:main",
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.9.1',
    ]
)
