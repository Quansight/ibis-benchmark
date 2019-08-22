#!/usr/bin/env python

import os

from setuptools import find_packages, setup

LONG_DESCRIPTION = """
Ibis Backend Benchmark
"""

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

version = "0.0.0"
with open(
    os.path.join(PROJECT_PATH, "ibis_benchmark", "__init__.py"), "r"
) as f:
    for l in f.readlines():
        if l.startswith("version"):
            version = l.split("=")[1].strip()

install_requires = [
    "click",
    "flake8",
    "ibis-framework",
    "isort",
    "seed-isort-config",
    "sh",
]

develop_requires = ["black", "pre-commit", "pytest"]

all_requires = install_requires + develop_requires

setup(
    name="ibis-benchmark",
    url="https://github.com/quansight/ibis-benchmark",
    packages=find_packages(),
    version=version,
    install_requires=install_requires,
    python_requires=">=3.6",
    extras_require={"all": all_requires, "develop": develop_requires},
    description="Ibis Benchmark",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    license="Apache License, Version 2.0",
    maintainer="Ivan Ogasawara",
    maintainer_email="ivan.ogasawara@quansight.com, ivan.ogasawara@gmail.com",
)
