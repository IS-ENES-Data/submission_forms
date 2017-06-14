from setuptools import setup, find_packages
import sys,os

setup(
   # FormFabric: DKRZ data submission form handler tools
   name="dkrz_forms",

   version="0.4.0",

   author="Stephan Kindermann",
   author_email="kindermann@dkrz.de",

   packages=find_packages(exclude=['ez_setup','test']),
   include_package_data=True,
   zip_safe=False,

   url="http://pypi.python.org/pypi/submission_forms_v040/",

   description = " Jupyter python notebook support code for data submission form handling",

   # Dependent Packages

   install_requires = ['gitpython', 'prov'], 

)

