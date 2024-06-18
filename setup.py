from setuptools import setup

setup(
    name="corelib",
    version="0.0.1",
    description="Library for interacting with Neo4j DB.",
    long_description=None,
    long_description_content_type=None,
    author="Ryland Sepic",
    author_email="TBD",
    url="https://github.com/magellanbot/guruai/tree/corelib-neo4j/src/CoreLib",
    license="None",  
    packages=["corelib"],  
    install_requires=[
        "iniconfig~=2.0",
        "neo4j~=5.19.0", # Minor version is a specifier requirement
        "neomodel~=5.3",
        "packaging~=24.0",
        "pytz~=2024.1"
    ],
    extras_require={
        "test": [
            "pluggy~=1.5",
            "pylint~=3.2",
            "pytest~=8.2",
            "pytest-mock~=3.14"
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Database",
    ],
)
