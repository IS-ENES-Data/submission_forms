# submission form jupyter notebook supporting code
# Author: S. Kindermann
# Version: 0.2 (March 2015)
# to do:
# separate out generic form code (e.g. git repo handling) as a super class
# from which specific form handlers inherit

"""
=============================================
Data submission information management tools
=============================================

Provided functionality:

* Information collection
* Information storage in git repo
* Jupyter notebook interface
* email / rt request tracker and git integration

Configuration:

* global variable setting in .dkrz_forms in home directoy
   * e.g. cordex_directoy = "path" specifies to git reop for project *cordex*

* use as library::

     from dkrz_forms import form_handler

* use in jupyter notebooks::

     from dkrz_forms import form_handler

     my_project = "CORDEX"
     form_handler.generate_submission_form(my_first_name,my_last_name,my_email,my_project)

  copies a jupyter notebook template for project "CORDEX" into your project repository


"""
# import all necessary libraries
# * most are in standard python library
# * others are imported conditionally
#
import os,sys,shutil,uuid
import pkg_resources
import socket
from datetime import datetime
try:
    from git import Repo,GitCommandError
except ImportError:
    print "Warning: please install git module with 'pip install gitpython'"
    print "otherwise all helper functions for interacting with git will not work"
join = os.path.join
import smtplib
from email.mime.text import MIMEText
import shelve
import json
import copy
import base64

# import non standard settings from home folder
# e.g. setting for project repositories like cordex_directory

from os.path import expanduser
home = expanduser("~")
sys.path.append(home + "/.dkrz_forms")

try:
  from myconfig import cordex_directory
  from myconfig import rt_pwd
  print "Settings from ~/.dkrz_forms imported"
  
except ImportError:
  print "Info: myconfig not found - taking default config "
  from config import cordex_directory

print "Your submission form repository:", cordex_directory


# load form checks
from tests import *

from dkrz_forms import tests

rt_module_present = False
try:
   import rt
   rt_module_present = True
except ImportError, e:
   pass

#------------------------------------------------------------------------------------------

# global variables defined and imported here, which are used in helper functions:
# cordex_directory, in general: "<project>_directory
# to be completed .. 
# generalized submission form class based on project dictionary defining to be defined variables

class submission_form(object):
    """
    generate a class based on dictionary, defining the project specific variables as well as their default values
    (motivation: syntactically more easy to set variables in notebook interface)

    example usage: cordex_submission_form = submission_form(cordex_dict)

    to do: separate module for project dictionaries and their corresponding tests
    """

    def __init__(self, proj_dict):
        for key,val in proj_dict.iteritems():
            self.__dict__[key]=val



def init_form(my_project,my_first_name,my_last_name,my_email,my_keyword):
    ''' initialize a submission form object based on a project dictionary
        and associate it with a git repo, where it is stored and maintained

        to do: move it to a class function !?
    '''
    if my_project == "CORDEX":
         from project_cordex import cordex_dict

         #sf = cordex_submission_form()
         sf = submission_form(cordex_dict)
         # initialize form object with location of git repo where submission forms are stored (locally)
         sf.sub['repo'] = cordex_directory
         # empty dictionary containing future submission specific information
         # like status, repo, etc. 
         sf.project='CORDEX'
         sf.sub['last_name']=my_last_name
         sf.sub['email']=my_email
         sf.sub['keyword']=my_keyword
           
         sf.sub['form_name']=my_last_name+'_'+my_keyword
         sf.sub['form_path']=sf.sub['repo']+'/'+sf.sub['form_name']+'.ipynb'
         
         sf.sub['id'] = str(uuid.uuid1())
            # print sf
        
         "to do: check availability of cordex_directoy and whether it is git versioned"

         print "Cordex submission form intitialized: sf"
         print "(For the curious: sf is used to store and manage all your information)"
        
         return sf

    if my_project =="test":
         from myconfig import test_dict
         sf = submission_form(test_dict)
        
         sf.sub['repo'] = cordex_directory

         print "Cordex submission form intitialized: sf"
         print "(For the curious: sf is used to store and manage all your information)"
          
         return sf


def generate_submission_form(my_first_name,my_last_name,my_email,my_project,my_keyword):
    ''' take project notebook template, rename it and copy the result to the
        projects submission form directory as a personal copy for the end user
    '''
        #working_dir = os.getcwd()
      # global variable cordex_directoy used here .. to be improved ..
    
   # from dkrz_forms import form_handler
    if my_project == "CORDEX":
        
          from project_cordex import cordex_dict
        
          sf = submission_form(cordex_dict)
          # initialize form object with location of git repo where submission forms are stored (locally)
          sf.sub['repo'] = cordex_directory
          sf.project='CORDEX'
          sf.sub['last_name']=my_last_name
          sf.sub['email']=my_email
          sf.sub['keyword']=my_keyword
           
          sf.sub['form_name']=my_last_name+'_'+my_keyword
          sf.sub['form_path']=sf.sub['repo']+'/'+sf.sub['form_name']+'.ipynb'
         
          sf.sub['id'] = str(uuid.uuid1())
            # print sf
        
          try:
              sf.sub['source_path'] = os.path.join(pkg_resources.get_distribution("dkrz_forms").location,"dkrz_forms/Templates/CORDEX_submission_form.ipynb")
          except:
              sf.sub['source_path'] = "/home/stephan/Repos/ENES-EUDAT/submission_forms/dkrz_forms/Templates/CORDEX_submission_form.ipynb"
              print "Attention: non standard source for submission forms, taking:", sf.sub['source_path']
              
          
          #print sf.__dict__
         
          print "copy from:", sf.sub['source_path']
          print "to: ", sf.sub['form_path']
          shutil.copyfile(sf.sub['source_path'],sf.sub['form_path'])
          print "--------------------------------------------------"
          print "submission form created, please visit the following link:"
          # print sf
          print "https://qc.dkrz.de:8080/notebooks/"+my_project+"/"+sf.sub['form_name']
          ## to do email link to user ....
          print "--------------------------------------------------"
          form_save(sf)
        
          repo = Repo(sf.sub['repo'])
          # get commit hash and add to json package
          master = repo.head.reference
          commit_hash = master.commit.hexsha
          sf.sub['commit_hash'] = commit_hash
           
          form_save(sf)
               
           
          if is_hosted_service():
               email_form_info(sf)
           
    else:
        print "--------------xxx------------------------------------"
        print "currently only submission forms for the project \"CORDEX\" are supported"
        print "no submission form created"
        print "please re-evaluate cell with proper project information"





def prefix_dict(mydict,prefix,keys):
    ''' Return a copy of a submission object with specified keys prefixed by a namespace
      to do: makes no senso fo sf objects - work on dicts instead ... 
    '''
    pr_dict = {}
    for key in keys:
        pr_dict[prefix + ':' + key] = mydict[key]
    return pr_dict

# Functions to convert form objects into dictionaries into json files and back

class Struct(object):
    def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)
        for k, v in adict.items():
           if isinstance(v, dict):
              self.__dict__[k] = Struct(v)
              
class FStruct(object):
  def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)
    
def dict_to_form(mydict):
  """
   converts a recursive dictionary to a (flat) python object, with dictionary properties
  """
  return FStruct(mydict)
  
def dict_to_hform(mydict):
    """
    converts a recursive dictionary to a recursive python object, with object properties
    """
    return Struct(mydict)
    

def form_to_json(sf):
    """
    serialize form value object to json string
    """
    s = json.dumps(sf.__dict__,sort_keys=True, indent=4, separators=(',', ': '))
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

def json_to_form(mystring):
    return dict_to_form(json_to_dict(mystring))

#----------------------------------------------------------------------------   

# functions to store form objects in git repo

def form_save(sf):
    """
     Commit form and associated json data package to git repo
    """
    #print "input for formsave", sf.__dict__
    repo = Repo(sf.sub['repo'])
    sf.sub['status'] = "stored"
    sf.sub['timestamp']=str(datetime.now())
   # .. should be defined prior to "save"
   # sf.sub['form_name']=sf.last_name+"_"+sf.sub['keyword']
    sf = package_submission(sf)
    #if check_form_name(sf):
    if True:
       try:
           ## to do: change this to: git add last_name__pre_name* 
           ## ..... - reuse form for mulltiple transmissions ?
           ## to do: first commit notebook - remember commit sha1 - add sha1 to json
           ## and commit json ... 
           ## sha = repo.head.object.hexsha
           ## later: may be helper function to retrieve notebook according to sha1 value of
           ## corresponding submitted json ...
           result = repo.git.add(sf.sub['form_name']+'*')
           #print result 
          
           commit = repo.git.commit(message='Submission form for user '+sf.last_name+' saved in repository:'+sf.sub['form_name'])
           #print commit         
           print "\n\n Status message:"
           print "-- your submission form "+sf.sub['form_name']+ " was stored in repository "
           #print "your associated data package "+sf.sub['package_name']+"\n was stored in repository "
          
       except GitCommandError:
           print "Error ! Please correct the form name (best copy and paste name from top of this page and add .ipynb extension)"


def is_hosted_service():
    hostname = socket.gethostname()
    if hostname == "qc.dkrz.de":
      return True
    else:
      return False

def email_form_info(sf):
  if is_hosted_service():
     m_part1 = "You edited and saved a CORDEX submission form\n"
     m_part2 = "This form is accessible at: \n"
     m_part3 = "https://qc.dkrz.de:8080/notebooks/CORDEX/"+sf.form_name+".ipynb \n"
     m_part4 = "to officially submit this form to be processed by DKRZ please follow the instructions in the submission part of the form \n"
     m_part5 = "in case of problems please contact data@dkrz.de"
     my_message = m_part1 + m_part2 + m_part3 + m_part4 + m_part5
     msg = MIMEText(my_message)
     msg['Subject'] = 'Your CORDEX data submission form'
     msg['From'] = "data_submission@dkrz.de"
     msg['To'] = sf.email
     # Send the message via the qc VM SMTP server, but don't include the\n"
     # envelope header.\n",
     s = smtplib.SMTP('localhost')
     s.sendmail("data_submission@dkrz.de", ["kindermann@dkrz.de"], msg.as_string())
     s.quit()
     print "Form submitted to your email address "+sf.email
  else:
     print "This form is not hosted at DKRZ! form email service is not available ! \n"


def form_submission(sf):
   """
     - submit to rt system in case RT module is present (True for DKRZ hosted service, probably false for home installations)
     - submit to "data_submission@dkrz" in case RT is not present but email is configured on installation
     - print instructions for manual submission in case all above is not working
   """


   if rt_module_present:
      tracker = rt.Rt('https://dm-rt.dkrz.de/REST/1.0/','kindermann',base64.b64decode("Y2Y3RHI2dlM="))
      ticket_id = tracker.create_ticket(Queue="CORDEX", Subject="CORDEX data submission: "+sf.institution+"--"+sf.lastname,
                  Priority= 10,Owner="kindermann@dkrz.de")
      sf.sub['ticket_id'] = ticket_id
      sf.sub['ticket_url'] = "https://dm-rt.dkrz.de/Ticket/Display.html?id="
      sf.sub['status']= "submitted"
      sf = packet_submission(sf)

      comment_submitted = tracker.comment(ticket_id, text=sf.institution+"--"+sf.lastname,files=[(json_file_name,open(sf.sub['package_path'],'rb'))])

      if not comment_submitted:
         sf.sub['status']= "rt-submission error"


   # generate updated json file and store in repo

   if not(rt_module_present) and is_hosted_service():
      m_part1 = "A CORDEX data submission was requested by: " + sf.first_name + " " + sf.last_name + "\n"
      m_part2 = "Corresponding email: "+ sf.email +"\n"
      m_part3 = "Submission form url: https://qc.dkrz.de:8080/notebooks/CORDEX/"+sf.form_name+".ipynb \n"
      m_part4 = "The submission is commited to the CORDEX submission form git repository with the name "+sf.form_name +"\n"
      m_part5 = "Time of submission:"+ str(datetime.now())

      my_message = m_part1 + m_part2 + m_part3 + m_part4 + m_part5
      msg = MIMEText(my_message)
      msg['Subject'] = 'Test email from DKRZ data submission form management software - please ignore'
      msg['From'] = "data_submission@dkrz.de"
      msg['To'] = sf.email
      msg['CC'] = "kindermann@dkrz.de"
      # Send the message via the qc VM SMTP server, but don't include the\n"
      # envelope header.\n",
      s = smtplib.SMTP('localhost')
      s.sendmail("data_submission@dkrz.de", ["kindermann@dkrz.de"], msg.as_string())
      s.quit()

      #  origin = repo.remotes.origin
      #  origin.push()
      #  print "Data submission form sent"
      #  print "A confirmation message will be sent to you"
   else:
      print "Please send form: "+cordex_directory+"/"+sf.form_name +"\n"
      print "as well as data package: "+sf.sub['package_path']+"\n"
      print "to data@dkrz.de with subject \"Cordex data submission form \""

def package_submission(sf):
    form_json = form_to_json(sf)
    #parts=sf.form_name.split(".")
    my_form_name = sf.sub['form_name']+".json"
    file_name = sf.sub['repo']+"/"+my_form_name
    form_file = open(file_name,"w+")
    form_file.write(form_json)
    form_file.close()
    sf.sub['package_path']=file_name
    sf.sub['package_name']=my_form_name
    print "form stored in transfer format in: "+file_name
    return sf


def unpackage_submission(sf):
    """
     untested
    """
    parts=sf.form_name.split(".")
    my_form_name = parts[0]
    file_name = cordex_directory+"/"+my_form_name+".json"
    form_file = open(file_name,"r")
    json_info = form_file.read(form_json)
    json_info["__type__"] = "sf",
    form_file.close()
    sf = json.loads(json_info)

    return sf

def persist_form(form_object,location):
    p_shelve = shelve.open(location)
    p_shelve['form_object'] = form_object
    p_shelve.close()

def get_form(location):
    p_shelve = shelve.open(location)
    form_object = p_shelve['form_object']
    p_shelve.close()
    return form_object



