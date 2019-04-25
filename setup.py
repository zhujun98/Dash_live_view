"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
import os
import re
from setuptools import setup, find_packages


_project_name = 'dash_live'

def find_version():
    with open(os.path.join(_project_name, '__init__.py')) as fp:
        for line in fp:
            m = re.search(r'^__version__ = "(\d+\.\d+\.\d[a-z]*\d*)"', line, re.M)
            if m is not None:
                return m.group(1)
        raise RuntimeError("Unable to find version string.")


setup(
    name=_project_name,
    version=find_version(),
    author='Jun Zhu',
    author_email='zhujun981661@gmail.com',
    description='',
    long_description='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
        ],
    },
    package_data={
        _project_name: ['templates/*.html']
    },
    install_requires=[
        "dash>=0.41.0",
        "flask>=1.0.2",
        "flask_caching>=1.7.1"
    ],
    extras_require={
        'docs': [
          'sphinx',
          'nbsphinx',
          'ipython',  # For nbsphinx syntax highlighting
        ],
        'test': [
          'pytest',
          'pytest-cov',
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ]
)
