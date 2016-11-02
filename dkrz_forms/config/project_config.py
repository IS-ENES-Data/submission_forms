# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:11:02 2016

@author: stephan

ToDo: Merge with variable tests ...
"""
# name spaces for w3c prov transformation of submission provenance information
from os.path import join as join
import base64

name_space={'sub':'http://enes.org/entities/ingest-workflow#',
            'ing':'http://enes.org/entities/ingest-workflow#',
            'qua':'http://enes.org/entities/ingest-workflow#',
            'pub':'http://enes.org/entities/ingest-workflow#',        
            'wf':'http://enes.org/entities/ingest-workflow#',        
            'dm':'http://enes.org/entities/ingest-workflow#',        
            'dp':'http://enes.org/entities/ingest-workflow#',        
            'node':'http://enes.org/entities/ingest-workflow#',        
            }
 
# adapt to your deployment           
install_directory = "/opt/formhandler/"
dir_prefix = "/opt/formhandler/Repos/"
info_db_path = join(dir_prefix,"db/db.json")

submission_directory = join(dir_prefix,"data_forms_repo")
user_submission_directory = join(dir_prefix,"submission_forms_repo")

# rest is deployment independent
project_directory = {}
project_directory["CORDEX"] = join(user_submission_directory,"CORDEX")
project_directory["CMIP6"] = join(user_submission_directory,"CMIP6")
project_directory["ESGF_replication"] = join(user_submission_directory,"ESGF_replication")
project_directory["DKRZ_CDP"] = join(user_submission_directory,"DKRZ_CDP")
project_directory["test"] = join(user_submission_directory,"test")


rt_pwd = base64.b64decode("Y2Y3RHI2dlM=")
#print project_directory
#print "general project config imported"

from dkrz_forms.config import workflow_steps 

# (submission,ingest,checking,publish) = form_handler.get_workflow_steps()

#print "./dkrz_forms:  workflow steps config imported"

project_dicts = {}
# submitted information
project_dicts['CORDEX']  = {
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
             'sub':workflow_steps.submission,
             'ing':workflow_steps.data_ingest,
             'qua':workflow_steps.qua,
             'pub':workflow_steps.publication            
             }


generic_dict = {
             "first_name":""
             }
             
# to do: put generic info in generic_dict and merge this with 
#        the project_dicts below
project_dicts['DKRZ_CDP'] = {
             'project': 'CMIP6_CDP',
             'sub':workflow_steps.submission,
             'ing':workflow_steps.data_ingest,
             'qua':workflow_steps.qua,
             'pub':workflow_steps.publication
 
 }
project_dicts['test'] = {
             'project' : "test",
             'sub':workflow_steps.submission,
             'ing':workflow_steps.data_ingest,
             'qua':workflow_steps.qua,
             'pub':workflow_steps.publication
 
 }
project_dicts['CMIP6']= {
             'project' : 'CMIP6',
             'sub':workflow_steps.submission,
             'ing':workflow_steps.data_ingest,
             'qua':workflow_steps.qua,
             'pub':workflow_steps.publication

 }            
 
project_dicts['ESGF_replication']= {
             'project' : 'CMIP6_replication',
             'sub':workflow_steps.submission,
             'ing':workflow_steps.data_ingest,
             'qua':workflow_steps.qua,
             'pub':workflow_steps.publication

 }            

#============= Definition of CORDEX specific test functions ===================================

