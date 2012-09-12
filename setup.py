from distutils.core import setup
from setuptools import find_packages

setup(
    name='cartridge-tax',
    version='0.0.1a',
    author='Kenneth Bolton',
    author_email='kenbolton@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='http://pypi.python.org/pypi/cartridge-tax/',
    license='LICENSE.txt',
    description='A tax module for Cartridge.',
    long_description=open('README.md').read(),
    dependency_links = [
        'http://github.com/htj/suds-htj/tarball/master#egg=suds-0.4.1-htj'
    ],
    install_requires=[
        "cartridge >= 0.6.0",
        "suds >= 0.4.1-htj",
    ],
    include_package_data=True,
    zip_safe=False,
)
