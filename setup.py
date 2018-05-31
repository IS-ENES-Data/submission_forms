from setuptools import setup, find_packages
import sys,os

setup(
   # FormFabric: DKRZ data submission form handler tools
   name="dkrz_forms",
   version="0.8.0",
   author="Stephan Kindermann",
   author_email="kindermann@dkrz.de",
   packages=find_packages(exclude=['ez_setup',',dist','test','install']),
   # packages=['dkrz_forms'],
   include_package_data=True,
   zip_safe=False,  
   url="https://github.com/IS-ENES-Data/submission_forms",
   description = " Jupyter python notebook support code for data submission form handling",   
   license = "Apache License Version 2.0",
   # Dependent Packages
   install_requires = ['gitpython', 'prov'],
   scripts=['bin/init_forms']

)

