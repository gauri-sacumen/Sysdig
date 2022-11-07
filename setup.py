"""Setup file for SysDig Secure Connector.

This will create a wheel file with the module name as `sysdig_connector`
"""
from setuptools import setup

PACKAGE_NAME = "secureEvents_connector"
py_typed = ["py.typed"]

setup(
    packages={
        f"{PACKAGE_NAME}": py_typed,
        f"{PACKAGE_NAME}.controller": py_typed,
        f"{PACKAGE_NAME}.utils": py_typed,
    },
    install_requires=[],
    setup_requires=["pytest-runner"],
)
