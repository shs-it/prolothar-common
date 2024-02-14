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

### Git Branching Model

We use [Git-flow](https://danielkummer.github.io/git-flow-cheatsheet/index.html) as our branching model.

### Deployment

```bash
make clean_package || make package && make publish
```

## Versioning

We use [SemVer](http://semver.org/) for versioning.

Given a version number MAJOR.MINOR.PATCH, increment the:
* MAJOR version when you make incompatible API changes
* MINOR version when you add functionality in a backward compatible manner
* PATCH version when you make backward compatible bug fixes

## Authors

* **Boris Wiegand** - boris.wiegand@stahl-holding-saar.de


