import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="advisory",
    version="0.0.2",
    author="Antonio Germán Márquez Trujillo",
    author_email="amtrujillo@us.es",
    description="Una herramienta para el análisis de vulnerabilidades en proyectos software open-source",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GermanMT/advisory",
    packages=setuptools.find_namespace_packages(include=['famapy.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        'bs4>=0.0.1',
        'graphviz>=0.19.1',
        'requests>=2.27.1',
        'z3-solver>=4.8.14.0',
        'nvdlib>=0.5.6',
        'python-dotenv>=0.20.0',
        'famapy>=0.7.0'
    ]
)