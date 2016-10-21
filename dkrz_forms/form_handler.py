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
import os,sys,shutil,uuid
import glob
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
config_dir = os.path.join(expanduser("~"),".dkrz_forms")
sys.path.append(config_dir)

try:
  from project_config import project_directory, install_directory, project_dicts, submission_directory
  
#  from myconfig import rt_pwd
# print "project config imported"
  
except ImportError:
#  print "Info: myconfig not found - taking default config "
  from dkrz_forms.config.project_config import project_directory, install_directory, project_dicts, submission_directory
  
# print "Your submission form repository:", project_directory


# load form checks
from checks import *

#from dkrz_forms import checks
#from dkrz_forms.config import workflow_steps

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


def init_form(my_project,my_first_name,my_last_name,my_email,my_keyword):
    ''' initialize a submission form object based on a project dictionary
        and associate it with a git repo, where it is stored and maintained

        to do: move it to a class function !?
    '''
    
    if my_project in ["CORDEX","CMIP6","CMIP6_replication","DKRZ_CDP","test"]:
         

         #sf = cordex_submission_form()
         sf = Form(project_dicts[my_project])
         # initialize form object with location of git repo where submission forms are stored (locally)
         sf.sub.repo = project_directory[my_project]
         # empty dictionary containing future submission specific information
         # like status, repo, etc. 
         sf.project=my_project
         sf.sub.last_name=my_last_name
         sf.sub.email=my_email
         sf.sub.keyword=my_keyword
           
         sf.sub.form_name=my_project+'_'+my_last_name+'_'+my_keyword
                 
         is_packaged = package_submission(sf,comment_on=False)
         
         "to do: check availability of cordex_directoy and whether it is git versioned"
         if is_packaged: 
             print "submission form intitialized: sf"
             print "(For the curious: the sf object is used in the following to store and manage all your information)"
        
         else:
             print "Please correct above errors, before proceeding"
             
         return sf     

def generate_submission_form(my_first_name,my_last_name,my_email,my_project,my_keyword):
    ''' take project notebook template, rename it and copy the result to the
        projects submission form directory as a personal copy for the end user
    '''
        #working_dir = os.getcwd()
      # global variable cordex_directoy used here .. to be improved ..
    
   # from dkrz_forms import form_handler
    

    
    if my_project in ["CORDEX","CMIP6","CMIP6_replication","DKRZ_CDP","test"]:
        
                    
          sf = Form(project_dicts[my_project])
          sf.project=my_project
          
          print "Form Handler: Initialized form for project:", my_project
          # print sf.__dict__
          # initialize form object with location of git repo where submission forms are stored (locally)
          sf.sub.repo = project_directory[my_project]       
          sf.sub.last_name=my_last_name
          sf.sub.email=my_email
          sf.sub.keyword=my_keyword
          sf.sub.form_name=my_project+'_'+my_last_name+'_'+my_keyword
          #sf.sub.form_path=sf.sub.repo+'/'+sf.sub.form_name+'.ipynb'
          sf.sub.form_path=os.path.join(sf.sub.repo,sf.sub.form_name+'.ipynb')
          sf.sub.id = str(uuid.uuid1())
           
          template_name = my_project+"_submission_form.ipynb"
          try:
              sf.subsource_path = os.path.join(pkg_resources.get_distribution("dkrz_forms").location,"dkrz_forms/Templates"+template_name)
          except:
              sf.sub.source_path = os.path.join(install_directory,"submission_forms/dkrz_forms/Templates",template_name)
              #print "Form Handler: Attention !  non standard source for submission form"
         
          #print "--- copy from:", sf.sub.source_path
          #print "--- to: ", sf.sub.form_path
          shutil.copyfile(sf.sub.source_path,sf.sub.form_path)
          print "--------------------------------------------------------------------"
          print "   A submission form was created for you, please visit the following link:"
          # print sf
          print "    https://data-forms.dkrz.de:8080/notebooks/"+my_project+"/"+sf.sub.form_name+".ipynb"
          ## to do email link to user ....
          print "--------------------------------------------------------------------"
          save_form(sf, "Form Handler: form - initial generation - quiet" )
        
          repo = Repo(sf.sub.repo)
          # get commit hash and add to json package
          master = repo.head.reference
          commit_hash = master.commit.hexsha
          sf.sub.commit_hash = commit_hash
           
          save_form(sf, "Form Handler: form - initial generation - commit hash added - quiet")
           
          if is_hosted_service():
               email_form_info(sf)
           
    else:
        print "--------------xxx------------------------------------"
        print "currently only submission forms for the following projects are supported: CORDEX,CMIP6,DKRZ_CDP,test,CMIP6_replication"
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

class Form(object):
    def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)
        for k, v in adict.items():
           if isinstance(v, dict):
              self.__dict__[k] = Form(v)
              
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
 
## todo: generalize in a recursive function definition ....   
def form_to_dict(sf):
    new_sf = copy.deepcopy(sf)
    new_sf.sub = new_sf.sub.__dict__
    new_sf.ing = new_sf.ing.__dict__
    new_sf.qua = new_sf.qua.__dict__
    new_sf.pub = new_sf.pub.__dict__
    return new_sf.__dict__
    
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
   
   
    #print "input for formsave", sf.__dict__
    repo = Repo(sf.sub.repo)
    #sf.sub['status'] = "stored"
    sf.sub.timestamp = str(datetime.now())
    # .. should be defined prior to "save"
    # sf.sub['form_name']=sf.last_name+"_"+sf.sub['keyword']
    if comment_on: 
       print "\n\nForm Handler - save form status message:"
    is_packaged = package_submission(sf,comment_on)
   
    #if check_form_name(sf):
    if is_packaged:
       try:
           ## to do: change this to: git add last_name__pre_name* 
           ## ..... - reuse form for mulltiple transmissions ?
           ## to do: first commit notebook - remember commit sha1 - add sha1 to json
           ## and commit json ... 
           ## sha = repo.head.object.hexsha
           ## later: may be helper function to retrieve notebook according to sha1 value of
           ## corresponding submitted json ...
       
           result = repo.git.add(sf.sub.repo+"/"+sf.project+"_"+sf.sub.last_name+"_"+"*")
           #result = repo.git.add(sf.sub.form_name+'*')
           #print result 
           
           commit_message =  "Form Handler: submission form for user "+sf.sub.last_name+" saved using prefix "+sf.sub.form_name + " ## " + comment
           commit = repo.git.commit(message=commit_message)
           if comment_on:
               print " --- commit message:"+ commit         
           
           #print "-- your submission form "+sf.sub.form_name+ " was stored in repository "
           #print "your associated data package "+sf.sub['package_name']+"\n was stored in repository "
          
       except GitCommandError:
           print "Error ! Please correct the form name (best copy and paste name from top of this page and add .ipynb extension)"


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
     msg['From'] = "data_submission@dkrz.de"
     msg['To'] = sf.sub.email
     # Send the message via the data-forms VM SMTP server, but don't include the\n"
     # envelope header.\n",
     s = smtplib.SMTP('localhost')
     s.sendmail("data_submission@dkrz.de", ["kindermann@dkrz.de"], msg.as_string())
     s.quit()
     print "Form submitted to your email address "+sf.sub.email
  else:
     print "This form is not hosted at DKRZ! Thus form information is stored locally on your computer \n"
     print "Here is a summary of the generated and stored information:"
     print "-- form for project: ",sf.project
     print "-- form name: ",sf.sub.form_name
     print "-- submission form path: ", sf.sub.subform_path 
     print "-- package path: ", sf.sub.package_path
     print "-- package name: ", sf.sub.package_name


def form_submission(sf):
   """
     - submit to rt system in case RT module is present (True for DKRZ hosted service, probably false for home installations)
     - submit to "data_submission@dkrz" in case RT is not present but email is configured on installation
     - print instructions for manual submission in case all above is not working
   """
   ## to do: validity check first
   shutil.copy(sf.sub.subform_path,submission_directory)
   shutil.copy(sf.sub.package_path,submission_directory)
   repo = Repo(submission_directory)
   repo.git.add(sf.project+"_"+sf.sub.last_name+"*")
   commit_message =  "Form Handler: submission form for user "+sf.sub.last_name+" saved using prefix "+sf.sub.form_name + " ## " 
   commit = repo.git.commit(message=commit_message)
   print commit
   result = repo.git.push()
   print result
   
   if rt_module_present:
      tracker = rt.Rt('https://dm-rt.dkrz.de/REST/1.0/','kindermann',base64.b64decode("Y2Y3RHI2dlM="))
      tracker.login()
      ticket_id = tracker.create_ticket(Queue="TestQueue", Subject="CORDEX data submission: "+sf.institution+"--"+sf.sub.last_name,
                  Priority= 10,Owner="kindermann@dkrz.de")
      sf.sub.ticket_id = ticket_id
      sf.sub.ticket_url = "https://dm-rt.dkrz.de/Ticket/Display.html?id="
      sf.substatus = "submitted"
      is_packaged = package_submission(sf,comment_on=False)
      json_file_name = sf.sub.form_name+".json"
      comment_submitted = tracker.comment(ticket_id, text=sf.institution+"--"+sf.sub.last_name,files=[(json_file_name,open(sf.sub.package_path,'rb'))])

      if not comment_submitted:
         sf.sub.status = "rt-submission error"


   # generate updated json file and store in repo

   if not(rt_module_present) and is_hosted_service():
      m_part1 = "A "+sf.myproject+"data submission was requested by: " + sf.first_name + " " + sf.last_name + "\n"
      m_part2 = "Corresponding email: "+ sf.email +"\n"
      m_part3 = "Submission form url: https://data-forms.dkrz.de:8080/notebooks/"+sf.projectCORDEX+"/"+sf.form_name+".ipynb \n"
      m_part4 = "The submission is commited to the following git repository: "+sf.form_name +"\n"
      m_part5 = "Time of submission:"+ str(datetime.now())

      my_message = m_part1 + m_part2 + m_part3 + m_part4 + m_part5
      msg = MIMEText(my_message)
      msg['Subject'] = 'Test email from DKRZ data submission form management software - please ignore'
      msg['From'] = "data_submission@dkrz.de"
      msg['To'] = sf.email
      msg['CC'] = "kindermann@dkrz.de"
      # Send the message via the data-forms VM SMTP server, but don't include the\n"
      # envelope header.\n",
      s = smtplib.SMTP('localhost')
      s.sendmail("data_submission@dkrz.de", ["kindermann@dkrz.de"], msg.as_string())
      s.quit()

      #  origin = repo.remotes.origin
      #  origin.push()
      #  print "Data submission form sent"
      #  print "A confirmation message will be sent to you"
   else:
      print "Please send form: "+sf.sub.subform_path +"\n"
      print "as well as data package: "+sf.sub.package_path+"\n"
      print "to data@dkrz.de with subject \"Cordex data submission form \""

def package_submission(sf,comment_on):
       
    
    pattern = sf.sub.repo+"/"+sf.project+"_"+sf.sub.last_name+"_"+"*"+".ipynb"
    
    paths = [n for n in glob.glob(pattern) if os.path.isfile(n)]
    
    ## check if multiple possible master files exist ????
    
    if len(paths) > 0:
             sf.sub.id = str(uuid.uuid1())
             form_json = form_to_json(sf)
             #parts=sf.form_name.split(".")
             my_jsonform_name = sf.sub.form_name+".json"
             sf.sub.subform_path=paths[0]
             file_path = sf.sub.repo+"/"+my_jsonform_name
             sf.sub.package_path = file_path
             sf.sub.package_name = my_jsonform_name
             
            
             form_file = open(file_path,"w+")
             form_file.write(form_json+"\r\n")
             form_file.close()
             if comment_on:
                   print " --- form stored in transfer format in: "+file_path
             return True
    else:
       print "Error: "
       print "your contact details are inconsistent with the form template you are using !"
       print "Either change your contact details, or the form template name" 
       print "(klick on name at the top of the page besides the jupyter logo)"
       print ""
       print "The template naming should be: "+sf.project+"_\"my_last_name\""+"_keyword"
       print "The _keyword part of the template name can differ form \"my_keyword\" you provided above" 
       return False
       
    


def persist_form(form_object,location):
    p_shelve = shelve.open(location)
    p_shelve['form_object'] = form_object
    p_shelve.close()

def get_form(location):
    p_shelve = shelve.open(location)
    form_object = p_shelve['form_object']
    p_shelve.close()
    return form_object

# load workflow steps 
def load_workflow_form(workflow_json_file): 

    workflow_dict = jsonfile_to_dict(workflow_json_file)
    
    workflow = Form(workflow_dict) 
    
    return workflow

# to do: functions to display status info of submission objects (and next steps in workflow)


