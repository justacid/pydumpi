import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pydumpi",
    version="0.0.1",
    author="Tobias Schwackenhofer",
    author_email="tobiasschw@gmail.com",
    description="Python bindings for the sst-dumpi trace format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justacid/pydumpi",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    )
)
