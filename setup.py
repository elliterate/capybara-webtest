import os
from setuptools import setup, find_packages
import sys


tests_require = []

driver_verification_tests_require = [
    "flaky",
    "flask",
    "py",
    "pytest ~= 3.0, != 3.3.*, < 3.5",
    "werkzeug"]
if sys.version_info < (3, 3):
    driver_verification_tests_require.append("mock")

tests_require += driver_verification_tests_require


def read(filename):
    """
    Returns the contents of the given package file.

    Args:
        filename (str): The name of the file to read, relative to the current
            directory.

    Returns:
        str: The contents of the given package file.
    """

    path = os.path.join(os.path.dirname(__file__), filename)

    with open(path) as f:
        return f.read()


def get_version():
    """ str: The package version. """

    global_vars = {}

    # Compile and execute the individual file to prevent
    # the package from being automatically loaded.
    source = read(os.path.join("capybara_webtest", "version.py"))
    code = compile(source, "version.py", "exec")
    exec(code, global_vars)

    return global_vars['__version__']


setup(
    name="capybara-webtest",
    version=get_version(),
    description="WebTest driver for Capybara",
    long_description=read("README.rst"),
    url="https://github.com/elliterate/capybara-webtest",
    author="Ian Lesperance",
    author_email="ian@elliterate.com",
    license="MIT",
    keywords="capybara webtest",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["capybara-py", "webtest", "xpath-py >= 0.0.4"],
    setup_requires=["pytest-runner"],
    tests_require=tests_require,
    extras_require={
        # Expose test dependencies for external scripts, like pip.
        "test": tests_require})
