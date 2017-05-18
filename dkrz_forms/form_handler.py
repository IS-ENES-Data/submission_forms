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
   * e.g. project_directoy = "path" specifies to git reop for project *cordex*

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

from __future__ import print_function
import abc
import os,sys,shutil,uuid
from os.path import join as join
from os.path import expanduser
import glob
import pkg_resources
import socket
import string
import random
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import shelve
import json
import copy
import base64


# automatically detect installed optional dependencies
# move to utils
dep = {}
try:
    from git import Repo,GitCommandError
    dep['git'] = True    
except ImportError:
    print("Warning: to use git based form versioning please install git module with 'pip install gitpython'")
    print("otherwise all helper functions for interacting with git will not work")
    dep['git'] = False

config_file = os.path.join(expanduser("~"),".dkrz_forms")
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

# To DO: use cerberos type checking
#

VERBOSE = True
#VERBOSE = False
def vprint(*txt):
    if VERBOSE:
        print(*txt)
    return

# import non standard settings from home folder
# e.g. setting for project repositories like cordex_directory 

if dep['config_file']:  
  from settings import INSTALL_DIRECTORY,  SUBMISSION_REPO, NOTEBOOK_DIRECTORY
  from settings import FORM_URL_PATH, FORM_REPO
else: 
  from dkrz_forms.config.settings import INSTALL_DIRECTORY,  SUBMISSION_REPO, NOTEBOOK_DIRECTORY
  from dkrz_forms.config.settings import FORM_URL_PATH, FORM_REPO 
  
from dkrz_forms.config.project_config import PROJECT_DICT  
  
from dkrz_forms.config import workflow_steps
from checks import *





#------------------------------------------------------------------------------------------


def init_sf(init_form):
    
          # generate an empty form 
          sf = Form({})
          
          # generate the project specific form
          form = Form(PROJECT_DICT[init_form['project']])

          # fill project name and workflow forms
          sf.project = init_form['project']
          sf.workflow = form.workflow
          sf.__doc__ = form.__doc__
          for (short_name,wflow_step) in form.workflow:
              setattr(sf,short_name ,Form(workflow_steps.WORKFLOW_DICT[wflow_step]))
              
              
              
          sf.sub.entity_out.form = form    
          
          sf.sub.entity_out.form_repo = join(FORM_REPO, init_form['project'])
          sf.sub.submission_repo = join(SUBMISSION_REPO, init_form['project'])
          sf.form_dir = join(NOTEBOOK_DIRECTORY, init_form['project'])
          
          print("Form Handler: Initialized form for project:", init_form['project'])
          vprint(sf.project)
          
          sf.sub.agent.last_name = init_form['last_name']
          sf.sub.agent.first_name= init_form['first_name']
          sf.sub.agent.email= init_form['email']
          
          sf.sub.activity.keyword=init_form['key']
          sf.sub.activity.pwd=init_form['pwd']
          
          sf.sub.entity_out.pwd = init_form['pwd']
         
          sf.sub.entity_out.form_name = init_form['project']+'_'+init_form['last_name']+'_'+init_form['key']
          sf.sub.entity_out.form_json = join(sf.sub.entity_out.form_repo,sf.sub.entity_out.form_name+'.json')
          #sf.sub.form_path=sf.sub.form_repo+'/'+sf.sub.form_name+'.ipynb'
          vprint(sf.sub.entity_out.form_repo)
          vprint(sf.sub.entity_out.form_name+'.ipynb')
          sf.sub.entity_out.form_repo_path=join(sf.sub.entity_out.form_repo,sf.sub.entity_out.form_name+'.ipynb')
          
          vprint("entity_in.form_path", sf.form_dir)
          sf.sub.entity_in.form_path=join(sf.form_dir,sf.sub.entity_out.form_name+'.ipynb') 
          sf.sub.entity_in.form_json=join(sf.form_dir,sf.sub.entity_out.form_name+'.json') 
          
          #sf = set_doc(sf)
          
          return(sf)


def init_form(init_form):
    ''' used in form notebooks
        initialize a submission form object based on a project dictionary
        and associate it with a git repo, where it is stored and maintained

        to do: move it to a class function !?
    '''
    
    if init_form['project'] in ["CORDEX","CMIP6","ESGF_replication","DKRZ_CDP","test"]:
         
         sf = init_sf(init_form)
         print("entity_out.form_repo:",sf.sub.entity_out.form_repo)
         print("entity_out:form:json:", sf.sub.entity_out.form_json)
                 
         is_packaged = package_submission(sf,comment_on=False)
         
         "to do: check availability of cordex_directoy and whether it is git versioned"
         if is_packaged: 
             print("submission form intitialized: sf")
             print("(For the curious: the sf object is used in the following to store and manage all your information)")
        
         else:
             print("Please correct above errors, before proceeding")
             
         return sf     
    else:
         print("please correct project specification, should be one of CORDEX,CMIP6,ESGF_replication,DKRZ_CP or test")
         sf = {}
         return sf

def generate_submission_form(init_form):
    ''' used in form generation notebook
        take project notebook template, rename it and copy the result to the
        projects submission form directory as a personal copy for the end user
    '''
        #working_dir = os.getcwd()
      # global variable cordex_directoy used here .. to be improved ..
    
   # from dkrz_forms import form_handler

    
    if init_form['project'] in ["CORDEX","CMIP6","ESGF_replication","DKRZ_CDP","test"]:
        
        
          init_form['pwd'] = id_generator()
          sf = init_sf(init_form)          
          keystore_path =  join(FORM_REPO,'keystore') 
         
          if os.path.isfile(keystore_path+'.dat'):
              keystore = get_persisted_info('forms_pwd',keystore_path)
          else:
              keystore = {}
              vprint("Warning: no keystore - new keystore generated")
          key_info = copy.deepcopy(init_form)
          key_info['form_name']= sf.sub.entity_out.form_name
          key_info['form_repo']= sf.sub.entity_out.form_repo
          key_info['form_json']= join(sf.sub.entity_out.form_repo,sf.sub.entity_out.form_name+'.json')
          key_info['form_path']= join(sf.sub.entity_out.form_repo,sf.sub.entity_out.form_name+'.ipynb')
          
          keystore[init_form['pwd']] = key_info
          vprint("TTT:  store key in keystore",init_form['pwd'],keystore_path)
          persist_info('forms_pwd',keystore,keystore_path)
        
           
          template_name = init_form['project']+"_submission_form.ipynb"
          try:
              sf.sub.entity_in.source_path = join(pkg_resources.get_distribution("dkrz_forms").location,"dkrz_forms/Templates"+template_name)
          except:
              sf.sub.entity_in.source_path = join(INSTALL_DIRECTORY,"submission_forms","dkrz_forms","Templates",template_name)
              #print "Form Handler: Attention !  non standard source for submission form"
          ## to do: version of template
          # sf.sub.entity_in.version = ...
          print("--- copy from:", sf.sub.entity_in.source_path)
          print("--- to: ", sf.sub.entity_out.form_path, sf.sub.entity_out.form_repo_path)
          print("--- too: ",   sf.sub.entity_in.form_path)
          shutil.copyfile(sf.sub.entity_in.source_path,sf.sub.entity_out.form_repo_path)
          shutil.copyfile(sf.sub.entity_in.source_path,sf.sub.entity_in.form_path)
          print("--------------------------------------------------------------------")
          print("   A submission form was created for you, please visit the following link:")
          # print sf
          print(FORM_URL_PATH+init_form['project']+'/'+sf.sub.entity_out.form_name+'.ipynb')
          ## to do email link to user ....
          print("--------------------------------------------------------------------")
          
          
         
          save_form(sf, "Form Handler: form - initial generation - quiet" )
          vprint(" ......  initial version saved ...")
              
          if dep['git']: 
              repo = Repo(sf.sub.entity_out.form_repo)
              # get commit hash and add to json package
              master = repo.head.reference
              commit_hash = master.commit.hexsha
              sf.sub.activity.commit_hash = commit_hash
               
              save_form(sf, "Form Handler: form - initial generation - commit hash added - quiet")
              print("  !!  current version saved in repository") 
              print("  !!  the above link is only valid for the next 5 hours")
              print("  !!  to retrieve the form after this use the following link: ")
              print("       http://localhost:888/notebooks.tst " )
              print("       with the password:", init_form['pwd'] )
              vprint("id: ", sf.sub.entity_out.pwd)
              if is_hosted_service():
                   email_form_info(sf)
          else:
              print("Warning: no version information stored")
              print("Install git and gitpython to enable this")
              
          return sf    
                
    else:
        print("--------------xxx------------------------------------")
        print("currently only submission forms for the following projects are supported: CORDEX,CMIP6,DKRZ_CDP,test,ESGF_replication")
        print("no submission form created")
        print("please re-evaluate cell with proper project information")
        return("Error")



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

# Functions to convert form objects into dictionaries into json files and back

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
        
        
#------to be integrated in code: fixed slot Form generation -------------------- 

def myprop(x, doc):
    def getx(self):
        return getattr(self, '_' + x)

    def setx(self, val):
        setattr(self, '_' + x, val)

    def delx(self):
        delattr(self, '_' + x)

    return property(getx, setx, delx, doc)

#class C(object):
#    #__metaclass__=abc.ABCMeta
#    a = myprop("a", "Hi, I'm A!")
#    b = myprop("b", "Hi, I'm B!")
#    
#    
#C.d = myprop("d","....DDDDDDDDDDDDDDDD......")



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



#test = Form_fixed_Generator(['x'])

#test.x = 10
#text.y = 20 

#-------------------------------------------------------------------------------       
          
              
class FForm(object):
  def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)
    
#def dict_to_form(mydict):
#  """
#   converts a recursive dictionary to a (flat) python object, with dictionary properties
#  """
#  return FForm(mydict)
  
#def dict_to_hform(mydict):
#    """
#    converts a recursive dictionary to a recursive python object, with object properties
#    """
#    return Form(mydict)
 

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

#----------------------------------------------------------------------------   

# functions to store form objects in git repo

def save_form(sf,comment):
    """
     Commit form and associated json data package to git repo
    """
    comment_on = True
    if comment.endswith("quiet"):
      comment_on = False
   
    if comment_on: 
       print("\n\nForm Handler - save form status message:")
    is_packaged = package_submission(sf,comment_on)
   
    #if check_form_name(sf):
    if is_packaged and dep['git']:
        repo = Repo(sf.sub.entity_out.form_repo)
        sf.sub.timestamp = str(datetime.now())

        try:
           ## to do: change this to: git add last_name__pre_name* 
           ## ..... - reuse form for mulltiple transmissions ?
           ## to do: first commit notebook - remember commit sha1 - add sha1 to json
           ## and commit json ... 
           ## sha = repo.head.object.hexsha
           ## later: may be helper function to retrieve notebook according to sha1 value of
           ## corresponding submitted json ...
       
           result1 = repo.git.add(sf.sub.entity_out.form_repo_path)
           result2 = repo.git.add(sf.sub.entity_out.form_json)
           
           #result = repo.git.add(sf.sub.form_name+'*')
           vprint(result1,result2)
           # !! to do: check result 1 - if ipynb was changed or not !!!
           
           commit_message =  "Form Handler: submission form for user "+sf.sub.agent.last_name+" saved using prefix "+sf.sub.entity_out.form_name + " ## " + comment
           commit = repo.git.commit(message=commit_message)
           if comment_on:
               print(" --- commit message:"+ commit)              
           
           #print "-- your submission form "+sf.sub.form_name+ " was stored in repository "
           #print "your associated data package "+sf.sub['package_name']+"\n was stored in repository "
          
        except GitCommandError:
           print("Error ! Please correct the form name (best copy and paste name from top of this page and add .ipynb extension)")
           
    else:
         vprint("saving without committing to a git repo")
        
    
    return sf 

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


def form_submission(sf):
   """
     - submit to rt system in case RT module is present (True for DKRZ hosted service, probably false for home installations)
     - submit to "DATA_SUBMISSION@dkrz" in case RT is not present but email is configured on installation
     - print instructions for manual submission in case all above is not working
   """
   ## to do: validity check first
   form_source = sf.sub.entity_out.form_repo_path
   json_source = sf.sub.entity_out.form_json
   form_target = join(SUBMISSION_REPO,sf.project)
   json_target = join(SUBMISSION_REPO,sf.project)
   
   form_name = sf.sub.entity_out.form_name
   shutil.copy(form_source,form_target)
   shutil.copy(json_source,json_target)
   
   if dep['git']:
       repo = Repo(join(SUBMISSION_REPO,sf.project))
       #repo.git.add(sf.project+"_"+sf.sub.last_name+"*")
       try: 
          o = repo.remotes.origin
          o.pull()
       except GitCommandError:
          print("Synchronization with global submission form repository failed !")
          pass
          
       except AttributeError:
          print("No global submission repo !!!")
          pass
          # to do: error handling
       
       repo.git.add(form_name+".ipynb")
       repo.git.add(form_name+".json")
       
       vprint(repo.git.status())
       #repo.git.add(join(sf.project,package_name)
       #repo.git.add(join(sf.project,form_name)
       commit_message =  "Form Handler: submission form for user "+sf.sub.agent.last_name+" saved using prefix "+ form_name+ " ## " 
       try: 
           commit = repo.git.commit(message=commit_message)
           vprint(commit)
       except GitCommandError:
           print("Commit in submissin repo failed")
           pass
          
      
       try: 
           result = repo.git.push()
           vprint(result)
          
       except GitCommandError:
           print("Push to global submission repo failed !")
           pass       
       
       except AttributeError:
          print("No global submission repo !!!") 
          pass
        
   else:
       print("Warning: submission was not stored and versioned in git repo")
      
   
   
   if dep['rt'] and is_hosted_service(): 
      vprint("Proceeding with ticket generation")
      tracker = rt.Rt('https://dm-rt.dkrz.de/REST/1.0/','kindermann',base64.b64decode("Y2Y3RHI2dlM="))
      tracker.login()
      ticket_id = tracker.create_ticket(Queue="TestQueue", Subject="DKRZ data form submission: "+sf.project+"--"+sf.sub.agent.last_name,
                  Priority= 10,Owner="kindermann@dkrz.de")
      sf.sub.activity.ticket_id = ticket_id
      sf.sub.activity.ticket_url = "https://dm-rt.dkrz.de/Ticket/Display.html?id="
      sf.sub.activity.status = "submitted"
      is_packaged = package_submission(sf,comment_on=False)
      json_file_name = sf.sub.form_name+".json"
      comment_submitted = tracker.comment(ticket_id, text=sf.project+"--"+sf.sub.agent.last_name,files=[(json_file_name,open(sf.sub.package_path,'rb'))])

      if comment_submitted:
         print("RT Ticket generated")
      else:
         print("RT Ticket generation failed")
         sf.sub.activity.error_status = "rt-submission error"


   # generate updated json file and store in repo
   
   if not(dep['rt']) and is_hosted_service():
      vprint("Proceeding with email generation")
      m_part1 = "A "+sf.myproject+"data submission was requested by: " + sf.sub.agent.first_name + " " + sf.sub.agent.last_name + "\n"
      m_part2 = "Corresponding email: "+ sf.email +"\n"
      m_part3 = "Submission form url: https://data-forms.dkrz.de:8080/notebooks/"+sf.projectCORDEX+"/"+sf.form_name+".ipynb \n"
      m_part4 = "The submission is commited to the following git repository: "+sf.form_name +"\n"
      m_part5 = "Time of submission:"+ str(datetime.now())

      my_message = m_part1 + m_part2 + m_part3 + m_part4 + m_part5
      msg = MIMEText(my_message)
      msg['Subject'] = 'Test email from DKRZ data submission form management software - please ignore'
      msg['From'] = "DATA_SUBMISSION@dkrz.de"
      msg['To'] = sf.email
      msg['CC'] = "kindermann@dkrz.de"
      # Send the message via the data-forms VM SMTP server, but don't include the\n"
      # envelope header.\n",
      s = smtplib.SMTP('localhost')
      s.sendmail("DATA_SUBMISSION@dkrz.de", ["kindermann@dkrz.de"], msg.as_string())
      s.quit()

      print("DKRZ forms request submitted")
      #  origin = repo.remotes.origin
      #  origin.push()
      #  print "Data submission form sent"
      #  print "A confirmation message will be sent to you"
      
      # set notebook and json file read only
      #os.chmod(sf.sub.subformpath,0o444)
      #os.chmod(sf.sub.packagepath,0o444) 
     

   if not(dep['rt']) and not(is_hosted_service()): 
      print("Please send form: "+sf.form_dir+"/"+form_name+".ipynb" +"\n")
      print("to data@dkrz.de with subject", "\"DKRZ data submission form for project\"", sf.project)
      
      
      
   # Modifications to submission object   
   sf.sub.entity_out.submission_form = join(SUBMISSION_REPO,sf.sub.entity_out.form_name+".ipynb")
   sf.sub.entity_out.submission_json = join(SUBMISSION_REPO,sf.sub.entity_out.form_name+".json")  
   
   return sf

def package_submission(sf,comment_on):
     '''
     store notebook and json file in form directory
     change sf.sub.id to identify this action (remove later .. !?)
     '''
     sf.sub.id = str(uuid.uuid1())
     form_json = form_to_json(sf) 
     vprint(sf.sub.entity_in.form_path)
     vprint(sf.sub.entity_out.form_repo_path)
     try:
         shutil.copyfile(sf.sub.entity_in.form_path,sf.sub.entity_out.form_repo_path)
     except:
         print("Error in file copy operation")
         print("Source: ",sf.sub.entity_in.form_path)
         print("Target: ",sf.sub.entity_out.form_repo_path)
         pass
     form_file = open(sf.sub.entity_out.form_json,"w+")
     form_file.write(form_json+"\r\n")
     form_file.close()
     if comment_on:
           print(" --- form stored in transfer format in: "+sf.sub.entity_out.form_json)
     return True
    #else:
    #   print("Error: ")
    #   print("your contact details are inconsistent with the form template you are using !")
    #   print("Either change your contact details, or the form template name")
    #   print("(klick on name at the top of the page besides the jupyter logo)")
    #   print("")
    #   print("The template naming should be: "+sf.project+"_\"my_last_name\""+"_keyword")
    #  print("The _keyword part of the template name can differ form \"my_keyword\" you provided above") 
    #   return False
       
    


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
    
    

# to do: functions to display status info of submission objects (and next steps in workflow)


