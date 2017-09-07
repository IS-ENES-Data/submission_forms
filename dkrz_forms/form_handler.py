# submission form jupyter notebook supporting code
# Author: S. Kindermann
# Version: 0.2 (March 2015)
# to do:
# separate out generic form code (e.g. git repo handling) as a super class
# from which specific form handlers inherit

"""
=============================================
Data submission form tools
=============================================

Supports the generation and evaluation of forms.
Forms are python notebook based and provide: 

* Information collection
* Information storage and management (json serialization, versioning)
* Jupyter notebook interfaces
* email / rt request tracker and git integration

Configuration:

* global variable settings in .settings in home directoy

* use as library or in juypter notebooks::

     from dkrz_forms import form_handler, utils
"""
# import all necessary libraries
# * most are in standard python library
# * others are imported conditionally
#

from __future__ import print_function
#import abc
import os,sys,shutil,uuid
from os.path import join as join
from os.path import expanduser
import glob
import pkg_resources

from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import shelve

import copy
import base64

from utils import Form, id_generator, form_to_json
from utils import is_hosted_service, email_form_info
from utils import persist_info, get_persisted_info
from utils import vprint, get_formurlpath
from utils import dep, is_hosted_service

try:
    from git import Repo,GitCommandError
except ImportError:
    print("Warning: to use git based form versioning please install git module with 'pip install gitpython'")
    print("otherwise all helper functions for interacting with git will not work")


called_with_env_variables = False

# ---------------------------

from dkrz_forms.config.project_config import PROJECT_DICT  
  
from dkrz_forms.config import workflow_steps
from checks import *


if dep['config_file']:  
  from settings import INSTALL_DIRECTORY,  SUBMISSION_REPO, NOTEBOOK_DIRECTORY
  from settings import FORM_DIRECTORY
    
else: 
  from dkrz_forms.config.settings import INSTALL_DIRECTORY,  SUBMISSION_REPO, NOTEBOOK_DIRECTORY
  from dkrz_forms.config.settings import FORM_DIRECTORY

if dep['rt']:
   import rt


# over-write variables in case Env settings are given
if os.getenv('INSTALL_DIRECTORY'):
    INSTALL_DIRECTORY = os.getenv('INSTALL_DIRECTORY')
    vprint("using env setting for INSTALL_DIRECTORY:",INSTALL_DIRECTORY)
    
if os.getenv('SUBMISSION_REPO'):
    INSTALL_DIRECTORY = os.getenv('SUBMISSION_REPO')
    vprint("using env setting for SUBMISSION_REPO:",SUBMISSION_REPO)

if os.getenv('NOTEBOOK_DIRECTORY'):
    INSTALL_DIRECTORY = os.getenv('NOTEBOOK_DIRECTORY')
    vprint("using env setting for NOTEBOOK_DIRECTORY:",NOTEBOOK_DIRECTORY)

if os.getenv('FORM_DIRECTORY'):
    INSTALL_DIRECTORY = os.getenv('FORM_DIRECTORY')
    vprint("using env setting for FORM_DIRECTORY:",FORM_DIRECTORY)    


FORM_REPO = FORM_DIRECTORY 
  



### detecting url of notebook server

FORM_URL_PATH = get_formurlpath()
   
    
#------------------------------------------------------------------------------------------

def init_sf(init_form):
            
          # generate the generic project form
          sf = Form(PROJECT_DICT[init_form['project']])
          # generate the submission infor sub_form
          form = Form(PROJECT_DICT[init_form['project']+'_FORM'])
          
          for (short_name,wflow_step) in sf.workflow:
              setattr(sf,short_name ,Form(workflow_steps.WORKFLOW_DICT[wflow_step]))
                             
          sf.sub.entity_out.report = form    
          
          sf.sub.entity_out.form_repo = join(FORM_REPO, init_form['project'])
          sf.sub.submission_repo = join(SUBMISSION_REPO, init_form['project'])
          sf.sub.form_dir = join(NOTEBOOK_DIRECTORY, init_form['project'])
          
          print("Form Handler: ")
          print ("    -- initializing form for project:", init_form['project'])
          vprint(sf.project)
          
          sf.sub.agent.last_name = init_form['last_name']
          sf.sub.agent.first_name= init_form['first_name']
          sf.sub.agent.email= init_form['email']
          
          sf.sub.activity.keyword=init_form['key']
          sf.sub.activity.pwd=init_form['pwd']
          sf.sub.activity.status="initialized"
          
          sf.sub.entity_out.pwd = init_form['pwd']
         
          sf.sub.entity_out.form_name = init_form['project']+'_'+init_form['last_name']+'_'+init_form['key']
          sf.sub.entity_out.form_json = join(sf.sub.entity_out.form_repo,sf.sub.entity_out.form_name+'.json')
          #sf.sub.form_path=sf.sub.form_repo+'/'+sf.sub.form_name+'.ipynb'
          vprint(sf.sub.entity_out.form_repo)
          vprint(sf.sub.entity_out.form_name+'.ipynb')
          sf.sub.entity_out.form_repo_path=join(sf.sub.entity_out.form_repo,sf.sub.entity_out.form_name+'.ipynb')
          
          vprint("entity_in.form_path", sf.sub.form_dir)
          sf.sub.entity_in.form_path=join(sf.sub.form_dir,sf.sub.entity_out.form_name+'.ipynb') 
          sf.sub.entity_in.form_json=join(sf.sub.form_dir,sf.sub.entity_out.form_name+'.json') 
          
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
         vprint("entity_out.form_repo:",sf.sub.entity_out.form_repo)
         vprint("entity_out.form.json:", sf.sub.entity_out.form_json)
                 
         is_packaged = package_submission(sf,comment_on=False)
         
         "to do: check availability of cordex_directoy and whether it is git versioned"
         if is_packaged: 
             print("    -- submission form intitialized")
             print("    -- (For the curious: the resulting sf object is used in the following")
             print("        to store and manage all your submission related information)")
        
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
              sf.sub.entity_in.source_path = join(pkg_resources.get_distribution("dkrz_forms").location,"dkrz_forms/Templates",template_name)
              vprint("taking pip installed template files")
          except:
              sf.sub.entity_in.source_path = join(INSTALL_DIRECTORY,"submission_forms","dkrz_forms","Templates",template_name)
              #print "Form Handler: Attention !  non standard source for submission form"
          ## to do: version of template
          # sf.sub.entity_in.version = ...
          print("--- copy from:", sf.sub.entity_in.source_path)
          print("--- to: ", sf.sub.entity_out.form_path, sf.sub.entity_out.form_repo_path)
          print("--- and to: ",   sf.sub.entity_in.form_path)
          shutil.copyfile(sf.sub.entity_in.source_path,sf.sub.entity_out.form_repo_path)
          shutil.copyfile(sf.sub.entity_in.source_path,sf.sub.entity_in.form_path)
          print("--------------------------------------------------------------------")
          print("   A submission form was created for you, please visit the following link:")
          # print sf
          print(FORM_URL_PATH+'/'+init_form['project']+'/'+sf.sub.entity_out.form_name+'.ipynb')
          ## to do email link to user ....
          print("--------------------------------------------------------------------")
          
          
         
          save_form(sf, "Form Handler: form - initial generation - quiet" )
          vprint(" ......  initial version saved ...")
          sf.sub.activity.status = "0-form_generated"
              
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
              print(FORM_URL_PATH+'/START/Retrieve_Form.ipynb' )
              print("       with the password:", init_form['pwd'] )
              
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



def form_submission(sf):
   """
     - submit to rt system in case RT module is present (True for DKRZ hosted service, probably false for home installations)
     - submit to "DATA_SUBMISSION@dkrz" in case RT is not present but email is configured on installation
     - print instructions for manual submission in case all above is not working
   """
   ## to do: validity check first
   target_dir = join(SUBMISSION_REPO,sf.project)
   vprint("Target dir: ", target_dir)
   form_source = sf.sub.entity_out.form_repo_path
   json_source = sf.sub.entity_out.form_json
   
   form_name = sf.sub.entity_out.form_name
   vprint("form_name: ", form_name)
   shutil.copy(form_source,target_dir)
   shutil.copy(json_source,target_dir)


   # also add selection files for replication
   if sf.project=="ESGF_replication":
     for sel_file in sf.sub.entity_out.report.selection_files:
         vprint("copy selection file - source:",join(sf.sub.entity_in.form_path,"selection",sel_file),"target: ", join(sf.sub.entity_out.form_repo,"selection"))
         shutil.copy(join(sf.sub.form_dir,"selection",sel_file),join(sf.sub.entity_out.form_repo,"selection"))
         vprint(" - and - copy selection file - source: ",join(sf.sub.entity_out.form_repo,"selection",sel_file), "target: ", join(target_dir,"selection"))
         shutil.copy(join(sf.sub.entity_out.form_repo,"selection",sel_file),join(target_dir,"selection"))
   
         

   if dep['git']:
       repo = Repo(SUBMISSION_REPO)
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
       
       repo.git.add(join(sf.project,form_name)+".ipynb")
       repo.git.add(join(sf.project,form_name)+".json")

       if sf.project=="ESGF_replication":
           for sel_file in sf.sub.entity_out.report.selection_files:
               vprint("commit selection file: ",join("selection",sel_file))
               repo.git.add(join(sf.project,"selection",sel_file))
       
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
      json_file_name = sf.sub.entity_out.form_name+".json"
      tracker = rt.Rt('https://dm-rt.dkrz.de/REST/1.0/','kindermann',base64.b64decode("Y2Y3RHI2dlM="))
      tracker.login()
      ticket_id = tracker.create_ticket(Queue="TestQueue", Subject="DKRZ data form submission: project="+sf.project+"  json-file="+json_file_name,
                  Priority= 10,Owner="kindermann@dkrz.de")
      sf.sub.activity.ticket_id = ticket_id
      sf.sub.activity.ticket_url = "https://dm-rt.dkrz.de/Ticket/Display.html?id="
      sf.sub.activity.status = "submitted"
      is_packaged = package_submission(sf,comment_on=True)
      vprint("open file: ", join(target_dir,json_file_name))
      comment_submitted = tracker.comment(ticket_id, text=sf.project+"--"+sf.sub.agent.last_name,files=[(json_file_name,open(sf.sub.entity_out.form_json,'rb'))])

      if comment_submitted:
         print("RT Ticket generated")
      else:
         print("RT Ticket generation failed")
         sf.sub.activity.error_status = "rt-submission error"


   # generate updated json file and store in repo
   
   if not(dep['rt']) and is_hosted_service():
      vprint("Proceeding with email generation")
      m_part1 = "A "+sf.myproject+"data submission was requested by: " + sf.sub.agent.first_name + " " + sf.sub.agent.last_name + "\n"
      m_part2 = "Corresponding email: "+ sf.sub.agent.email +"\n"
      m_part3 = "Submission form url: https://data-forms.dkrz.de:8080/notebooks/"+sf.projectCORDEX+"/"+sf.form_name+".ipynb \n"
      m_part4 = "The submission is commited to the following git repository: "+sf.form_name +"\n"
      m_part5 = "Time of submission:"+ str(datetime.now())
      my_message = m_part1 + m_part2 + m_part3 + m_part4 + m_part5
      msg = MIMEText(my_message)
      msg['Subject'] = 'Test email from DKRZ data submission form management software - please ignore'
      msg['From'] = "DATA_SUBMISSION@dkrz.de"
      msg['To'] = sf.sub.agent.email
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
      print("Please send form: "+sf.sub.form_dir+"/"+form_name+".ipynb" +"\n")
      print("to data@dkrz.de with subject", "\"DKRZ data submission form for project\"", sf.project)
      
      
      
   # Modifications to submission object   
   sf.sub.entity_out.submission_form = join(SUBMISSION_REPO,sf.sub.entity_out.form_name+".ipynb")
   sf.sub.entity_out.submission_json = join(SUBMISSION_REPO,sf.sub.entity_out.form_name+".json")  

   save_form(sf, "Submitted: final submission ..")
   email_form_info(sf)
   
   return sf

def package_submission(sf,comment_on):
     '''
     store notebook and json file in form directory
     change sf.sub.id to identify this action (remove later .. !?)
     '''
     sf.sub.id = str(uuid.uuid1())
     form_json = form_to_json(sf) 
     vprint(sf.sub.entity_in.form_path)
     vprint(sf.sub.entity_in.form_json)
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
       


