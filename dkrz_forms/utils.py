# -*- coding: utf-8 -*-
"""
Created on Fri May  5 15:24:05 2017

@author: stephan

modified from https://github.com/epigen/pypiper/blob/master/pypiper/AttributeDict.py
"""

import os

class Form(object):
    """
    A class to convert a nested Dictionary into an object 
    """
    def __init__(self, entries, default=False):
        """
        :param entries: A dictionary (key-value pairs) to add as attributes.
        :param default: set default values, if not specified default=False
        """
        self.add_entries(entries, default)
        self.return_defaults = default
      
    def add_entries(self, entries, default=False):
        for key, value in entries.items():
            if type(value) is dict:
                self.__dict__[key] = Form(value, default)
            else:
                self.__dict__[key] = value
#                in case shell variable expansion is required:                
#                try:
#                    # try expandvars() to allow the use of shell variables.
#                    self.__dict__[key] = os.path.expandvars(value)  # value
#                except TypeError:
#                    # if value is an int, expandvars() will fail; if 
#                    # expandvars() fails, just use the raw value
#                    self.__dict__[key] = value
    
    def __getitem__(self, key):
    		"""
    		Provides dict-style access to attributes
    		"""
    		return getattr(self, key)
    
    def __repr__(self):
    		return str(self.__dict__)
           
    
    def __getattr__(self, name):
            if name in self.__dict__.keys():
    		      return self.name
            else:
                if self.return_defaults:
			    # If this object has default mode on, then we should
			    # simply return the name of the requested attribute as
			    # a default, if no attribute with that name exists.
			    return name
                else:
                     raise AttributeError("No attribute " + name)

