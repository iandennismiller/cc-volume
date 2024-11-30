# Chromecast Controls

from setuptools import setup, find_packages

setup(
    version='0.1.0',
    name='chromecast-controls',
    description="Chromecast Controls",
    packages=find_packages(),
    scripts=[
        "scripts/cc-volume.py",
    ],
    include_package_data=True,
    keywords='',
    author="Ian Dennis Miller",
    author_email="",
    install_requires=[
        "pychromecast",
        "ttkthemes",
        "pyinstaller",
    ],
    license='proprietary',
    zip_safe=False,
)
