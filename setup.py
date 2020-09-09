from setuptools import setup, find_packages

setup(
    name="tasks",
    version="0.0.1",
    author="T. Bezemer",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        "redis>=3.5.3",
    ],
    extras_require={
        "dev" : [
            "pytest>=5.2.0"
        ]
    }
)