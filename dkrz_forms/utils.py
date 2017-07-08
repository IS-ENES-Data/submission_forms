# -*- coding: utf-8 -*-
"""
Created on Fri May  5 15:24:05 2017

@author: stephan

modified from https://github.com/epigen/pypiper/blob/master/pypiper/AttributeDict.py
"""
from __future__ import print_function
import os,sys
import json
import abc
import string, random
import socket
import smtplib
import shelve
import shutil
from os.path import expanduser
from email.mime.text import MIMEText
from prov.model import ProvDocument
#from dkrz_forms import form_handler

dep = {}
try:
    from git import Repo,GitCommandError
    dep['git'] = True    
except ImportError:
    print("Warning: to use git based form versioning please install git module with 'pip install gitpython'")
    print("otherwise all helper functions for interacting with git will not work")
    dep['git'] = False

config_file = os.path.join(expanduser("~"),".settings.py")
if os.path.isfile(config_file):
    sys.path.append(config_file)
    dep['config_file'] = True
else:
    dep['config_file'] = False
        
try:
   import rt
   dep['rt'] = True 
except ImportError, e:
   dep['rt'] = False   



VERBOSE=True
def vprint(*txt):
    if VERBOSE:
        print(*txt)
    return



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def prefix_dict(mydict,prefix):
    ''' Return a copy of a submission object with specified keys prefixed by a namespace
      to do: makes no senso fo sf objects - work on dicts instead ... 
    '''
    pr_dict = {}
    for key,val in mydict.iteritems():
        if (key != "__doc__") and not isinstance(val,dict):
            pr_dict[prefix + ':' + key] = mydict[key]
    return pr_dict


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
    
    print("workflow definition: ",sf_dict['workflow'])
    for [act_name,act] in sf_dict['workflow']:
        
        print("adding entities for workflow_step: ",act_name)
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
        entity_in_dict=prefix_dict(entity_in_dict,'subm')
        entity_out_dict=prefix_dict(entity_out_dict,'subm')
        agent_dict=prefix_dict(agent_dict,'subm')
        activity_dict=prefix_dict(activity_dict,'subm')
        
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
    ''' Form object with attributes defined by a configurable project dictionary
    '''
    __metaclass__=abc.ABCMeta
    def __init__(self, adict):
        """Convert a dictionary to a Form Object
        
        :param adict: a (hierarchical) python dictionary 
        :returns Form objcet: a hierachical Form object with attributes set based on input dictionary             
        """
        self.__dict__.update(adict)
        ## self.__dict__[key] = AttributeDict(**mydict)  ??
        for k, v in adict.items():
           if isinstance(v, dict):
              self.__dict__[k] = Form(v)
              
    def __repr__(self):
        """
        """
        return "DKRZ Form object "
        
    def __str__(self):
        return "DKRZ Form object: %s" %  self.__dict__



def form_to_dict(sf):
    result = {}
    for key, val in sf.__dict__.iteritems():
        
        if isinstance(val,Form):
           new_val = form_to_dict(val)
        else:
           new_val = val
        result[key] = new_val
    return result 
    
    
def form_to_json(sf):
    """
    serialize form value object to json string
    """
    sf_dict = form_to_dict(sf)
    
    s = json.dumps(sf_dict,sort_keys=True, indent=4, separators=(',', ': '))
    return s

def json_to_dict(mystring):
    """
    :param arg1: json string
    :type arg1: string
    :return: dictionary
    :rtype: dict

    """
    mydict = json.loads(mystring)
    return mydict
    
def jsonfile_to_dict(jsonfilename):
    jsonfile = open(jsonfilename,"r")
    json_info = jsonfile.read()
    jsonfile.close()
    json_dict = json.loads(json_info)
    return json_dict
    


def json_to_form(mystring):
    return FForm(json_to_dict(mystring))
    
    
    
#------------------------------------------------------------------------------------    

def is_hosted_service():
    hostname = socket.gethostname()
    if hostname == "data-forms.dkrz.de":
      return True
    else:
      return False

def email_form_info(sf):
  if is_hosted_service():
     m_part1 = "You edited and saved a form for project: "+sf.project+"\n"
     m_part2 = "This form is accessible at: \n"
     m_part3 = "https://data-forms.dkrz.de:8080/notebooks/"+sf.project+"/"+sf.sub.form_name+".ipynb \n"
     m_part4 = "to officially submit this form to be processed by DKRZ please follow the instructions in the submission part of the form \n"
     m_part5 = "in case of problems please contact data@dkrz.de"
     my_message = m_part1 + m_part2 + m_part3 + m_part4 + m_part5
     msg = MIMEText(my_message)
     msg['Subject'] = 'Your DKRZ data form for project: '+sf.project
     msg['From'] = "DATA_SUBMISSION@dkrz.de"
     msg['To'] = sf.sub.email
     # Send the message via the data-forms VM SMTP server, but don't include the\n"
     # envelope header.\n",
     s = smtplib.SMTP('localhost')
     s.sendmail("DATA_SUBMISSION@dkrz.de", ["kindermann@dkrz.de"], msg.as_string())
     s.quit()
     print("Form submitted to your email address "+sf.sub.email)
  else:
     print("This form is not hosted at DKRZ! Thus form information is stored locally on your computer \n")
     print("Here is a summary of the generated and stored information:")
     print("-- form for project: ",sf.project)
     print("-- form name: ",sf.sub.entity_out.form_name)
     print("-- submission form path: ", sf.sub.entity_out.subform_path)
     print("-- package path: ", sf.sub.entity_out.package_path)
     print("-- package name: ", sf.sub.entity_out.package_name)




#----------------------------------------------------------------------------------------------------------------------------

def persist_info(key,form_object,location):
    p_shelve = shelve.open(location)
    p_shelve[key] = form_object
    p_shelve.close()

def get_persisted_info(key,location):
    p_shelve = shelve.open(location)
    form_object = p_shelve[key]
    p_shelve.close()
    return form_object

# load workflow steps 
def load_workflow_form(workflow_json_file): 

    workflow_dict = jsonfile_to_dict(workflow_json_file)
    
    workflow = Form(workflow_dict) 
    
    return workflow


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def init_git_repo(target_dir):
    vprint("Initialize git repo:",target_dir)
    if os.path.exists(target_dir):
       shutil.rmtree(target_dir)
    if dep['git']:   
       repo = Repo.init(target_dir)
       return True
    else:
       os.makedirs(target_dir)
       print("Warning: form directory - ",target_dir," created - but no git versioning support")
       return False
    




#----- not used by now: may be replacement for class Form in future


class FForm(object):
  def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)

class TForm(object):
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


def myprop(x, doc):
    def getx(self):
        return getattr(self, '_' + x)

    def setx(self, val):
        setattr(self, '_' + x, val)

    def delx(self):
        delattr(self, '_' + x)

    return property(getx, setx, delx, doc)
    
    
def Form_fixed_Generator(slot_list):
    

    class Meta(type): 
        def __new__(cls, name, bases, dctn):
             dctn['__slots__'] = slot_list
             return type.__new__(cls, name, bases, dctn)
     
    class FixedForm(object):
         __metaclass__ = Meta

         def __init__(self):
            pass 
    
    fixed_form_object = FixedForm()
    
    return fixed_form_object  
    
    
    
    