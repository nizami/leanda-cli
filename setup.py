import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='leanda',
    version='0.0.1',
    scripts=['bin/leanda', 'bin/leanda.cmd'],
    author="ArqiSoft",
    author_email="info@arqisoft.com",
    description="Leanda Command Line Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArqiSoft/leanda-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
         "Operating System :: OS Independent",
    ],
)
