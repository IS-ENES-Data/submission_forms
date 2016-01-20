from setuptools import setup, find_packages
import sys,os

setup(
   # DKRZ data submission form handler
   name="dkrz_forms",

   version="0.1.0",

   author="Stephan Kindermann",
   author_email="kindermann@dkrz.de",

   packages=find_packages(exclude=['test']),
   include_package_data=True,

   url="http://pypi.python.org/pypi/form_handler_v010/",

   description = " Jupyter python notebook support code for data submission form handling",

   # Dependent Packages

   install_requires = [], 

)

