import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tactile_patterns",
    version="0.0.1",
    author="Mateusz Konieczny",
    author_email="matkoniecz@gmail.com",
    description="Generates tactile patterns recognisable by touch, for use in laser-cut designs. For people who are blind or with a poor eyesight, in dark.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matkoniecz/tactile_patterns",
    packages=setuptools.find_packages(),
    install_requires=[
        'jsbeautifier>=1.13.5, <2.0',
        'pyproj>=3.0, <4.0',
        'numpy>=1.19.5, <2.0',
        'pillow>=8.1.2, <9.0',
        # svgis is GPL licensed by called via shell without intimate communication
        # see
        # https://www.gnu.org/licenses/gpl-faq.html#GPLInProprietarySystem
        # https://www.gnu.org/licenses/gpl-faq.html#MereAggregation
        # that should apply and as far as I see explain that it is OK
        'svgis>=0.5.1',
    ],
    # use following to install that:
    # pip install --user -e .[dev]
    extras_require={
        'dev': [
            'pylint>=2.7.2',
            'autopep8>=1.5.6',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
