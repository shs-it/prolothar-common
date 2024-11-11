# Prolothar-Common

Common functionality for our ProLothar projects, which contain algorithms
for process mining and event sequence analysis tasks.

Visit [https://github.com/shs-it?q=prolothar](https://github.com/shs-it?q=prolothar)
to get a list of the ProLothar repositories.

## Usage

If you want to use this library, read the following instructions.

### Prerequisites

- Python 3.11+
- Depending on your system: C++ Compiler for compiling Cython code

### Installing

```bash
pip install prolothar-common
```

## Development

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Additional Prerequisites
- make (optional)

### Running the tests

```bash
make test
```

### Deployment

1. Change the version in version.txt
2. Build and publish the package on pypi by

```bash
make clean_package
make package && make publish
```

3. Create and push a tag for this version by

```bash
git tag -a $(cat version.txt) -m "describe this version"
git push --all && git push --tags
```

### Devcontainer

There is a decontainer definition in this project, which helps you to set up your environment.
At Stahl-Holding-Saar, we are behind a corporate proxy and cannot install dependencies from PyPi directly.
I yet have not found a stable solution to set the PIP_INDEX_URL and PIP_TRUSTED_HOST variables dynamically. 
In the current Dockerfile, I hardcoded the values, so you have to adapt them. 
If you know a solution to this problem, please contact me. 

## Versioning

We use [SemVer](http://semver.org/) for versioning.

Given a version number MAJOR.MINOR.PATCH, increment the:
* MAJOR version when you make incompatible API changes
* MINOR version when you add functionality in a backward compatible manner
* PATCH version when you make backward compatible bug fixes

## Authors

* **Boris Wiegand** - boris.wiegand@stahl-holding-saar.de


