# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:11:02 2016

@author: stephan

ToDo: Merge with variable tests ...
"""
# name spaces for w3c prov transformation of submission provenance information
from os.path import join as join
import base64

NAME_SPACES={'sub':'http://enes.org/entities/ingest-workflow#',
            'ing':'http://enes.org/entities/ingest-workflow#',
            'qua':'http://enes.org/entities/ingest-workflow#',
            'pub':'http://enes.org/entities/ingest-workflow#',        
            'wf':'http://enes.org/entities/ingest-workflow#',        
            'dm':'http://enes.org/entities/ingest-workflow#',        
            'dp':'http://enes.org/entities/ingest-workflow#',        
            'node':'http://enes.org/entities/ingest-workflow#',        
            }
 
# adapt to your deployment           

 
# directory where submission_forms package is installed
# leave empty if pip installed
# install_directory = "/opt/formhandler/"
INSTALL_DIRECTORY = "/home/stephan/Repos/ENES-EUDAT/"

# Directory where web accessible forms are served
NOTEBOOK_DIRECTORY = '/home/stephan/Repos/ENES-EUDAT/submission_forms/test/forms'

FORM_URL_PATH = 'http://localhost:8888/notebooks/Repos/ENES-EUDAT/submission_forms/test/forms/'
# Directory where the project git repos live
# dir_prefix = "/opt/formhandler/Repos/"
DIR_PREFIX = "/home/stephan/tmp/Repos/"    # for json db storage
INFO_DB_PATH = join(DIR_PREFIX,"db/db.json")

FORM_REPO = "/home/stephan/tmp/Repos/form_repo"

# final submissions repo (gitlab synchronized)
SUBMISSION_REPO = "/home/stephan/tmp/Repos/submission_repo"

# rest is deployment independent
#project_directory = {}
#project_directory["CORDEX"] = join(user_submission_directory,"CORDEX")
#project_directory["CMIP6"] = join(user_submission_directory,"CMIP6")
#project_directory["ESGF_replication"] = join(user_submission_directory,"ESGF_replication")
#project_directory["DKRZ_CDP"] = join(user_submission_directory,"DKRZ_CDP")
#project_directory["test"] = join(user_submission_directory,"test")


rt_pwd = base64.b64decode("Y2Y3RHI2dlM=")
#print project_directory
#print "general project config imported"

from dkrz_forms.config import workflow_steps 

# (submission,ingest,checking,publish) = form_handler.get_workflow_steps()

#print "./dkrz_forms:  workflow steps config imported"

PROJECT_DICT = {}

# submitted information
PROJECT_DICT['CORDEX']  = {
             "project":"CORDEX",
             "first_name": "",
             "last_name" : "",
             "email" : "",
             "submission_type" : "",
             "institution" : "",
             "institute_id" : "",
             "model_id" : "",
             "experiment_id" : "",
             "time_period" : "",
             "example_file_name" : "",
             "grid_mapping_name" : "",
             "grid_as_specified_if_rotated_pole" : "",
             "data_qc_status" : "",
             "data_qc_comment" : "",
             "terms_of_use" : "",
             "directory_structure" : "",
             "data_path" : "",
             "data_information" : "",
             "exclude_variables_list" : "",
             "variable_list_day" : "",
             "variable_list_mon" : "",
             "variable_list_sem" : "",
             "variable_list_fx" : "",
             "uniqueness_of_tracking_id" : "",
             "workflow": ["sub","ing","qua","pub"], 
             #'sub':workflow_steps.data_submission,
             #'ing':workflow_steps.data_ingest,
             #'qua':workflow_steps.data_quality_assurance,
             #S'pub':workflow_steps.data_publication  
             }
                         

generic_dict = {
             "first_name":""
             }
             
# to do: put generic info in generic_dict and merge this with 
#        the project_dicts below
PROJECT_DICT['DKRZ_CDP'] = {
             'project': 'CMIP6_CDP',
             "workflow" : ["sub","ing","qua","pub"]
 }
PROJECT_DICT['test'] = {
             'project' : "test",
             "workflow" : ["sub","ing","qua","pub"]
 }
PROJECT_DICT['CMIP6']= {
             'project' : 'CMIP6',
             "workflow" : ["sub","ing","qua","pub"]
 }            
 
PROJECT_DICT['ESGF_replication']= {
             'project' : 'CMIP6_replication',
             "workflow" : ["sub","ing","qua","pub"]
 }            

#============= Definition of CORDEX specific test functions ===================================

