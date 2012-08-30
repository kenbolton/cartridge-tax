from distutils.core import setup

setup(
    name='cartridge-tax',
    version='0.0.1a',
    author='Kenneth Bolton',
    author_email='kenbolton@gmail.com',
    packages=['cartridge-tax',],
    scripts=[],
    url='http://pypi.python.org/pypi/cartridge-tax/',
    license='LICENSE.txt',
    description='A tax package for Cartridge.',
    long_description=open('README.md').read(),
    install_requires=[
        "cartridge >= 0.6.0",
    ],
)
