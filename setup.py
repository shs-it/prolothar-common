# -*- coding: utf-8 -*-

#import order is important!
import pathlib
from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import os

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / "LICENSE").read_text()

with open(HERE / 'requirements.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.split('#', 1)[0].strip(' \t\n') for line in f
        ] if s != ''
    ] + ['Cython', 'scipy']

with open(HERE / 'version.txt', 'r') as f:
    version = f.read().strip()

def make_extension_from_pyx(path_to_pyx: str) -> Extension:
    return Extension(
        path_to_pyx.replace('/', '.').replace('.pyx', ''),
        sources=[path_to_pyx], language='c++')

if os.path.exists('prolothar_common/levenshtein.pyx'):
    extensions = [
        make_extension_from_pyx("prolothar_common/levenshtein.pyx"),
        make_extension_from_pyx("prolothar_common/mdl_utils.pyx"),
        make_extension_from_pyx("prolothar_common/longest_common_subsequence.pyx"),
        make_extension_from_pyx("prolothar_common/models/dataset/instance.pyx"),
        make_extension_from_pyx("prolothar_common/models/eventlog/event.pyx"),
        make_extension_from_pyx("prolothar_common/models/eventlog/complex_event.pyx"),
        make_extension_from_pyx("prolothar_common/models/eventlog/trace.pyx"),
        make_extension_from_pyx("prolothar_common/models/directly_follows_graph.pyx"),
        make_extension_from_pyx("prolothar_common/models/dfg/node.pyx"),
        make_extension_from_pyx("prolothar_common/models/dfg/edge.pyx"),
        make_extension_from_pyx("prolothar_common/models/diintgraph/directed_int_graph.pyx"),
        make_extension_from_pyx("prolothar_common/experiments/statistics.pyx"),
        make_extension_from_pyx("prolothar_common/collections/list_utils.pyx"),
        make_extension_from_pyx("prolothar_common/collections/tuple_utils.pyx"),
    ]
else:
    extensions = []

# This call to setup() does all the work
setup(
    name="prolothar-common",
    version=version,
    description="algorithms for process mining and data mining on event sequences",
    long_description=README,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url="https://github.com/shs-it/prolothar-common",
    author="Boris Wiegand",
    author_email="boris.wiegand@stahl-holding-saar.de",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["prolothar_common"],
    include_package_data=True,
    ext_modules=cythonize(extensions, language_level = "3", annotate=True),
    zip_safe=False,
    install_requires=install_reqs,
    extras_require={
        'ray': 'ray[default]'
    }
)
