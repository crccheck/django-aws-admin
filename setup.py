from setuptools import setup

setup(
    name='aws_admin',
    version='0.0.0',
    author='Chris Chang',
    author_email='c@crccheck.com',
    url='',
    packages=['aws_admin'],
    include_package_data=True,  # automatically include things from MANIFEST.in
    license='Apache License, Version 2.0',
    description='',
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
    ],
)
