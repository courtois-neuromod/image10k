from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="image10k",
    version="0.1",
    description="A dataset of annotated open images for cognitive neuroscience research",
    license="MIT",
    url="https://github.com/simexp/image10k",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Optional (see note above)
    project_urls={  # Optional
        "Bug Reports": "https://github.com/simexp/image10k/issues",
        "Funding": "https://cneuromod.ca",
        "Source": "https://github.com/simexp/image10k",
    },
    maintainer="Valentina Borghesani",
    maintainer_email="valentinaborghesani",
    packages=find_packages(),
    package_data={},
    install_requires=[
        "pandas>=1.4.1",
        "jupyter==1.0.0",
        "pandas==1.4.1",
        "requests==2.27.1",
        "argparse==1.4.0",
        "tqdm==4.62.3",
        "beautifulsoup4==4.10.0",
    ],  # external packages as dependencies
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Data",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.5",
)
