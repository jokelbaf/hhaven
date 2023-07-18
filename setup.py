"""Run setuptools."""
from setuptools import find_packages, setup

setup(
    name = "hhaven",
    version = "0.1.0",
    author = "jokelbaf",
    author_email = "jokelbaf@gmail.com",
    description = "A well-documented and typed API wrapper for Hentai Haven.",
    keywords = "hentai-haven hentai".split(),
    url = "https://github.com/jokelbaf/hhaven",
    project_urls = {
        "Documentation": "https://jokelbaf.github.io/hhaven",
        "API Reference": "https://jokelbaf.github.io/hhaven-api-reference",
        "Issue tracker": "https://github.com/jokelbaf/hhaven/issues",
    },
    packages = find_packages(exclude=["tests.*"]),
    python_requires = ">=3.8",
    install_requires = ["aiohttp", "pydantic", "aiocache"],
    include_package_data = True,
    package_data = {"hhaven": ["py.typed"]},
    long_description = open("README.md", encoding="utf-8").read(),
    long_description_content_type = "text/markdown",
    license = "MIT",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)