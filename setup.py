"""Setup file for UnleashClient"""
from setuptools import setup, find_packages


def readme():
    """Include README.rst content in PyPi build information"""
    with open('README.md') as file:
        return file.read()

setup(
    name='gitsecret',
    version='0.0.1',
    author='Ivan Lee',
    author_email='ivanklee86@gmail.com',
    description='Python wrapper for git-secret.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/ivanklee86/gitsecret',
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ]
)

