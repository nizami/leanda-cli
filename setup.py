import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='leanda',
    version='0.0.3',
    # py_modules=['leanda'],
    # scripts=['bin/leanda', 'bin/leanda.cmd'],
    include_package_data=True,
    packages=setuptools.find_packages(),
    author="ArqiSoft",
    author_email="info@arqisoft.com",
    description="Leanda Command Line Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArqiSoft/leanda-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
         "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        leanda=leanda.cli:cli
    ''',
)
