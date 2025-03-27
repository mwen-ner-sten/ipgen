from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ipgen",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A flexible IP address generator with multiple input/output formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "ipaddress>=1.0.23",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ipgen-gui=ipgen.gui:main",
        ],
    },
) 