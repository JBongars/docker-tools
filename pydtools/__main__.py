import setuptools

from pydtools import run


def get_readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


setuptools.setup(
    name="dtools",  # This is the name of the package
    version="1.5.0",  # The initial release version
    author="Julien Bongars",  # Full name of the author
    description="Use docker in your development workflow",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires='>=3.6',  # Minimum version requirement of the package
    py_modules=["dtools"],  # Name of the python package
    package_dir={'': 'quicksample/src'
                 },  # Directory of the source code of the package
    install_requires=[
        "certifi==2023.5.7",
        "charset-normalizer==3.1.0",
        "docker==6.1.2",
        "idna==3.4",
        "Jinja2==3.1.2",
        "MarkupSafe==2.1.2",
        "packaging==21.3",
        "pyparsing==3.0.9",
        "requests==2.31.0",
        "retrying==1.3.3",
        "six==1.16.0",
        "urllib3==2.0.2",
        "websocket-client==1.5.2",
    ]  # Install other dependencies if any
)

if __name__ == "__main__":
    run.run()