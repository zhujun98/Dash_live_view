"""
Author: Jun Zhu <zhujun981661@gmail.com>
"""
import os
import re
from setuptools import setup, find_packages


def find_version():
    with open(os.path.join('dash_live_view', '__init__.py')) as fp:
        for line in fp:
            m = re.search(r'^__version__ = "(\d+\.\d+\.\d[a-z]*\d*)"', line, re.M)
            if m is not None:
                return m.group(1)
        raise RuntimeError("Unable to find version string.")


setup(
    name='dash_live_view',
    version=find_version(),
    author='Jun Zhu',
    author_email='zhujun981661@gmail.com',
    description='',
    long_description='',
    url='',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
        ],
    },
    package_data={
    },
    install_requires=[
        "flask",
        "flask_caching"
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
