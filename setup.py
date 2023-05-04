from setuptools import setup, find_packages

setup(
    name="quantsight",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "langchain"
    ],
    python_requires=">=3.6",
)