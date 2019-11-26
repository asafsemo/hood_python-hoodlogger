from setuptools import setup

setup(
    name='hoodlogger',
    version='0.0.4',
    description='Hood Logger python package',
    package_dir={'': 'src'},
    packages=['hoodlogger'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'numpy>=1.17',
        'Flask>=1.1'
    ],
    url="https://github.com/asafsemo/hood_python-hoodlogger",
    author="Asaf Semo",
    author_email="asafsemo@gmail.com",
)
