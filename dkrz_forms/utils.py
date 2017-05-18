# -*- coding: utf-8 -*-
"""
Created on Fri May  5 15:24:05 2017

@author: stephan

modified from https://github.com/epigen/pypiper/blob/master/pypiper/AttributeDict.py
"""

import os
import json
from prov.model import ProvDocument
from dkrz_forms import form_handler

def gen_prov_graph(file_path,option):
    '''
      generates prov graph from form json file
      option = "all": add attribues to nodes
    '''
    form_file = open(file_path,"r")
    json_info = form_file.read()
    form_file.close()
    sf_dict = json.loads(json_info)
    
    d1=ProvDocument()
    d1.add_namespace('subm','http://www.enes.org/enes_entity/data_submsission')


    global_in_out = d1.entity("subm:"+"form_name_xx")
    
    for [act_name,act] in sf_dict['workflow']:
           
        entity_in_dict = sf_dict[act_name]['entity_in']
        entity_out_dict = sf_dict[act_name]['entity_out']
        agent_dict = sf_dict[act_name]['agent']
        activity_dict = sf_dict[act_name]['activity']
        
        # generate nodes
        in_node = d1.entity("subm:"+entity_in_dict['i_name'])
        out_node = d1.entity("subm:"+entity_out_dict['i_name'])
        agent = d1.agent("subm:"+agent_dict['i_name'])
        activity = d1.activity("subm:"+activity_dict['i_name'] )
        
        
        #clean up and prefix dictionaries
        entity_in_dict=form_handler.prefix_dict(entity_in_dict,'subm')
        entity_out_dict=form_handler.prefix_dict(entity_out_dict,'subm')
        agent_dict=form_handler.prefix_dict(agent_dict,'subm')
        activity_dict=form_handler.prefix_dict(activity_dict,'subm')
        
        if option=="all":
            in_node.add_attributes(entity_in_dict)
            out_node.add_attributes(entity_out_dict)
            agent.add_attributes(agent_dict)
            activity.add_attributes(activity_dict)
        
        # connect nodes in graph
        d1.wasGeneratedBy(out_node,activity)
        d1.used(activity,in_node)
        d1.wasAssociatedWith(activity,agent)
        d1.wasDerivedFrom(in_node,out_node)
        d1.used(activity,global_in_out)
        d1.wasGeneratedBy(global_in_out,activity)

    return d1






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

