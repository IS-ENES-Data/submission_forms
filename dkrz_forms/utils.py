# -*- coding: utf-8 -*-
"""
Created on Fri May  5 15:24:05 2017

@author: stephan

attribute dict related parts modified from https://github.com/epigen/pypiper/blob/master/pypiper/AttributeDict.py
"""
from __future__ import print_function
import os,sys,subprocess, getpass,json, abc, string,random
import socket,smtplib,shelve,shutil
import dkrz_forms.config.settings as settings
import dkrz_forms.config.project_config as project_config  
from dkrz_forms.config import workflow_steps
import distutils.dir_util
import pkg_resources
from os.path import expanduser, isfile, exists, join
#
from email.mime.text import MIMEText
from prov.model import ProvDocument


FORM_URL_PATH = join(settings.BASE_URL,getpass.getuser(),"notebooks","Forms")
if settings.SERVER == "notebook":
    FORM_URL_PATH = join(settings.BASE_URL,"notebooks","Forms")
#-------------------------------------------------------------------------------------------
""" Get information in installed dependencies
    information is collected in a the dictionary dep
"""
dep = {}
try:
    from git import Repo,GitCommandError, InvalidGitRepositoryError
    dep['git'] = True    
except ImportError:
    print("Warning: to use git based form versioning please install git module with 'pip install gitpython'")
    print("otherwise all helper functions for interacting with git will not work")
    dep['git'] = False

config_file = os.path.join(expanduser("~"),"settings.py")
if os.path.isfile(config_file):
    sys.path.append(config_file)
    dep['config_file'] = True
else:
    dep['config_file'] = False
        
try:
   import rt
   dep['rt'] = True 
except ImportError as e:
   dep['rt'] = False   


#-----------------------------------------------------------------
if dep['config_file']:  
  from settings import INSTALL_DIRECTORY,  SUBMISSION_REPO
  from settings import FORM_DIRECTORY, BASE_URL, SERVER
    
else: 
  from dkrz_forms.config.settings import INSTALL_DIRECTORY,  SUBMISSION_REPO
  from dkrz_forms.config.settings import FORM_DIRECTORY, BASE_URL, SERVER
#----------------------------------------------------------------------------------------

VERBOSE=True
def vprint(*txt):
    if VERBOSE:
        print(*txt)
    return
  
def init_home_env():
    '''
    initialize environment for jupyter notebooks:
        - directories
        - start notebook
    '''
    proj_dirs = project_config.PROJECTS
    dirs = [settings.NOTEBOOK_DIRECTORY,settings.SUBMISSION_REPO,settings.FORM_DIRECTORY]
   
    dst = join(os.environ['HOME'],'Forms')
    if INSTALL_DIRECTORY == 'pip': 
         print("Environment initialized from pip package information")
         src = join(pkg_resources.get_distribution("dkrz_forms").location,"dkrz_forms","Templates","Forms")
    else: 
        src = join(INSTALL_DIRECTORY, "submission_forms", "dkrz_forms", "Templates", "Forms")
        print("From: ...:",src)
    try: 
        shutil.copytree(src,dst)
        print("Environment initialized, to create a submission forms please open:")
        print(join(FORM_URL_PATH,"Create_Submission_Form.ipynb"))
        print("__________________________________________________________________")

            
        if dep['git']:
           try: 
              repo=Repo(settings.SUBMISSION_REPO)
           except InvalidGitRepositoryError:
              repo=Repo.init(settings.SUBMISSION_REPO)
              vprint("initialize: ", settings.SUBMISSION_REPO)
                
           #for proj_dir in proj_dirs:
           #    
           #     repo_dir = join(settings.FORM_DIRECTORY,proj_dir)
           #     try:
           #         repo=Repo(repo_dir)
           #     except InvalidGitRepositoryError:
           #        repo=Repo.init(repo_dir)
           #        vprint("initialize: ", repo_dir)
            
           #vprint("git directories initialized")       
        else: 
            print("Warning !!!!: please install git on your system")
             
    except OSError as why: 
       print("you initialized your environment already ! skipping initialization !")
       print(why)
    except FileExistsError as why:
       print("you initialized your environment already ! skipping initialization !!")
       print(why)
  
    
        
    
    
    
def init_config_dirs():
    '''
    initialize the directories for the project forms
    - deprecated, not used ...
    '''
 
    dirs = [settings.NOTEBOOK_DIRECTORY,settings.SUBMISSION_REPO,settings.FORM_DIRECTORY]
    proj_dirs = project_config.PROJECTS

    for dir in dirs:
       for proj_dir in proj_dirs:
           distutils.dir_util.mkpath(join(dir,proj_dir))
           # python3: pathlib.Path(mypath).mkdir(parents=True, exist_ok=True)
 
    if dep['git']:
       try: 
          repo=Repo(settings.SUBMISSION_REPO)
       except InvalidGitRepositoryError:
         repo=Repo.init(settings.SUBMISSION_REPO)
         vprint("initialize: ", settings.SUBMISSION_REPO)
            
       for proj_dir in proj_dirs:
           
            repo_dir = join(settings.FORM_DIRECTORY,proj_dir)
            try:
                repo=Repo(repo_dir)
            except InvalidGitRepositoryError:
               repo=Repo.init(repo_dir)
               vprint("initialize: ", repo_dir)
        
            try:
               repo=Repo(proj_dir)
            except InvalidGitRepositoryError:
               repo=Repo.init(repo_dir)
               vprint("initialize: ", repo_dir)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def prefix_dict(mydict,prefix):
    ''' Return a copy of a submission object with specified keys prefixed by a namespace
        to do: makes no sense for sf objects - work on dicts instead ... 
    '''
    pr_dict = {}
    for key,val in mydict.items():
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
    for key, val in sf.__dict__.items():
        
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
    

def generate_project_form(project):
    if project in project_config.PROJECTS:
        sf = Form(project_config.PROJECT_DICT[project])
        for (short_name,wflow_step) in sf.workflow:
                  setattr(sf,short_name ,Form(workflow_steps.WORKFLOW_DICT[wflow_step]))
        form = Form(project_config.PROJECT_DICT[project+'_FORM'])   
        sf.sub.entity_out.report = form
        return sf 
    else:
        print("Error: form generation failed")
        return Form({})
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
     m_part2 = "This form is acessible at: \n"
     m_part3 = FORM_URL_PATH+"/"+sf.project+"/"+sf.sub.entity_out.form_name+".ipynb \n"
     m_part4 = "status info: "+sf.sub.activity.status
     m_part5 = '''\n \nto officially submit this form to be processed by DKRZ please follow the instructions in the submission part of the form \n in case of problems please contact data-pool@dkrz.de'''

     if sf.sub.activity.status=="3:completed":
        m_part1 = "You have submitted a form for project: "+sf.project+"\n"
        m_part2 = "you should receive an automatic email with the notice of receipt \n"
        m_part3 = "In case you do not receive this email please contact data-pool@dkrz.de \n"
        m_part4 = "in this email please mention the following form identifier: "+sf.project+"/"+sf.sub.entity_out.form_name 
        m_part5 = ""
     my_message = m_part1 + m_part2 + m_part3 + m_part4 + m_part5 
     msg = MIMEText(my_message)
     msg['Subject'] = 'Your DKRZ data form for project: '+sf.project
     msg['From'] = "data-pool@dkrz.de"
     msg['To'] = sf.sub.agent.email
     # Send the message via the data-forms VM SMTP server, but don't include the\n"
     # envelope header.\n",
     s = smtplib.SMTP('localhost')
     s.sendmail("data-pool@dkrz.de", ["kindermann@dkrz.de",sf.sub.agent.email], msg.as_string())
     s.quit()
     print("The link to your form was sent to:"+sf.sub.agent.email)
  else:
     print("This form is not hosted at DKRZ! Thus form information is stored locally on your computer \n")
     print("Here is a summary of the generated and stored information:")
     print("-- form for project: ",sf.project)
     print("-- form name: ",sf.sub.entity_out.form_name)
     print("-- submission form path: ", sf.sub.entity_out.form_repo_path)
     print("-- json form path: ", sf.sub.entity_out.form_json)
     print("To officically submit this form please send these to files to data-pool@dkrz.de")




#----------------------------------------------------------------------------------------------------------------------------

def persist_info(form_object,location):
    p_shelve = shelve.open(location)
    p_shelve[form_object['pwd']] = form_object
    p_shelve.close()

def get_persisted_info(location):
    p_shelve = shelve.open(location)
    result = {}
    for key in p_shelve:
        result[key] = p_shelve[key] 
    p_shelve.close()
    return result

# load workflow steps 
def load_workflow_form(workflow_json_file): 
    ''' Load a json file and convert file to Form object '''

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
            if name in list(self.__dict__):
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
    
    
    
def get_file_list(file_list):
     # call synda to retrieve the dataset lists associated to synda selection files   
     print("This command should print a list of datasets in case you provided correct synda selection files")
     print("return to step 3 to chech your files in case of error messages")
     dataset_dict = {}
     for s_file in file_list: 
         dataset_dict[s_file]= subprocess.check_output(['synda', 'search', '-s', './selection/'+s_file])
     return dataset_dict
     result = []
     return(result)
