from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="quantsight",
    version="0.1.11",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "langchain",
        "data-cache",
        "openai",
        "tabulate"
    ],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type='text/markdown'
)
