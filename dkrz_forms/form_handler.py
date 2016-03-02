# submission form jupyter notebook supporting code
# Author: S. Kindermann
# Version: 0.1 (Dezember 2015) 
# to do:
# separate out generic form code (e.g. git repo handling) as a super class
# from which specific form handlers inherit

import os,sys,shutil,uuid
import pkg_resources
import socket
from datetime import datetime
from git import Repo,GitCommandError
join = os.path.join
import smtplib
from email.mime.text import MIMEText
import shelve
import json
from config import cordex_directory
from tests import *

class cordex_submission_form(object):
        """
          simple class object storing submission form values
          just for simple input of values in notebook interface
          downstream tools will use the json serialization of the values of this class
        """
	def __init__(self):
            
            self.first_name = ""
            self.last_name = ""
            self.email = ""
            self.submission_type = ""
            self.institution = ""
            self.institute_id = ""
            self.model_id = ""
            self.experiment_id = ""
            self.time_period = ""
            self.example_file_name = ""
            self.grid_mapping_name = ""
            self.grid_as_specified_if_rotated_pole = ""
            self.data_qc_status = ""
            self.data_qc_comment = ""
            self.terms_of_use = ""
            self.directory_structure = ""
            self.data_path = ""
            self.data_information = ""
            self.exclude_variables_list = ""
            self.variable_list_day = ""
            self.variable_list_mon = ""
            self.variable_list_sem = ""
            self.variable_list_fx = ""
            self.uniqueness_of_tracking_id = ""
            self.check_status="not checked"
            self.package_path=""
            self.package_name=""

def json_to_form(json_dict):
  """
  to be completed: use json.loads function, example:

  user = json.loads('{"__type__": "User", "name": "John Smith", "username": "jsmith"}')
  print user['name']
  print user['username']
  """

def form_to_json(sf):
    """ 
    serialize form value object to json string
    """
    s = json.dumps(sf.__dict__)
    return s

def json_to_dict(mystring):
    mydict = json.loads(mystring)
    return mydict

def cordex_file_info(sf,file_name):
  # cordex file structure:
  # VariableName_Domain_GCMModelName_CMIP5ExperimentName_CMIP5EnsembleMember_RCMModelName_RCMVersionID_Frequency[_StartTime - EndTime].nc
	    cordex_template=["VariableName","Domain","GCMModelName","CMIP5ExperimentName","CMIP5EnsembleMember","RCMModelName","RCMVersionID","Frequency","TimeRange"] 
	    cordex_example = "tas_EUR-44_MPI-M-MPI-ESM-LR_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19710101-19751231.nc"
	    cordex_example_parts = cordex_example.split("_") 
	    for i,part in enumerate(cordex_example_parts):
             print cordex_template[i],":",part


def check_form_name(sf):
    if sf.form_name == "...":
        return False
    else:
        return True

def form_save(sf,repo):
    """
     Commit form and associated json data package to git repo 
    """
    sf = package_submission(sf)
    if check_form_name(sf):
       try: 
           repo.git.add(sf.package_name)
           repo.git.add(sf.form_name)
           repo.git.commit(message='Submission form for user '+sf.first_name+"_"+sf.last_name+' saved in git repository:'+sf.form_name)
           print "submission form "+sf.form_name+"\n stored in local git repository "
           print "submission data "+sf.package_name+"\n stored in local git repository "
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
   if is_hosted_service():
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
      print "as well as data package: "+sf.package_path+"\n"
      print "to data@dkrz.de with subject \"Cordex data submission form \"" 

def package_submission(sf):
    form_json = form_to_json(sf)
    parts=sf.form_name.split(".")
    my_form_name = parts[0]
    file_name = cordex_directory+"/"+my_form_name+".json"
    form_file = open(file_name,"w+")
    form_file.write(form_json)
    form_file.close()
    sf.package_path=file_name
    sf.package_name=my_form_name+".json"
    # print "form stored in transfer format in: "+file_name
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

def init_form():
    sf = cordex_submission_form()
    # initialize form object with location of git repo where submission forms are stored (locally)
    repo = Repo(cordex_directory)           

    print "Cordex submission form intitialized ......"
    print "(technically a submission form (sf) object as well as a repository (repo object) are created to store the submission form)"
    return sf,repo

def generate_submission_form(my_first_name,my_last_name,my_email,my_project):
    ''' take project notebook template, rename it and copy the result to the 
        projects submission form directory as a personal copy for the end user
    '''
        #working_dir = os.getcwd()
    if my_project == "CORDEX":
           my_id = str(uuid.uuid1())
	   my_name = my_first_name+"_"+my_last_name
	   target_file_name=my_project+"__"+my_name+"__submission"+"__"+my_id+".ipynb"
 	   target = cordex_directory+"/"+target_file_name
	   #print target
	   #print source
           new_form_file = open(target,"w")
           source = os.path.join(pkg_resources.get_distribution("dkrz_forms").location,"dkrz_forms/Templates/CORDEX_submission_form.ipynb")

           
	   shutil.copyfile(source,target)
           print "--------------------------------------------------"
           print "submission form created, please visit the following link:"
           print "https://qc.dkrz.de:8080/notebooks/"+my_project+"/"+target_file_name
    else:
           print "--------------------------------------------------"
           print "currently only submission forms for the project \"CORDEX\" are supported"
           print "no submission form created"
           print "please re-evaluate cell with proper project information"
