# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:11:02 2016

@author: stephan

ToDo: Merge with variable tests ...
"""
# name spaces for w3c prov transformation of submission provenance information
name_space={'sub':'http://enes.org/entities/ingest-workflow#',
            'ing':'http://enes.org/entities/ingest-workflow#',
            'qua':'http://enes.org/entities/ingest-workflow#',
            'pub':'http://enes.org/entities/ingest-workflow#',        
            'wf':'http://enes.org/entities/ingest-workflow#',        
            'dm':'http://enes.org/entities/ingest-workflow#',        
            'dp':'http://enes.org/entities/ingest-workflow#',        
            'node':'http://enes.org/entities/ingest-workflow#',        
            }
            

project_directory = "/home/dkrz/k202015/Repos/forms"
install_directory = "/home/dkrz/k202015"
info_db_path = "/home/dkrz/k202015/db.json"

import base64
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

project_dicts['CMIP6_CDP'] = {
             'project': 'CMIP6_CDP',
             'sub':workflow_steps.submission,
             'ing':workflow_steps.data_ingest,
             'qua':workflow_steps.qua,
             'pub':workflow_steps.publication
 
 }
project_dicts['test_dict'] = {
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
 
project_dicts['CMIP6_replication']= {
             'project' : 'CMIP6_replication',
             'sub':workflow_steps.submission,
             'ing':workflow_steps.data_ingest,
             'qua':workflow_steps.qua,
             'pub':workflow_steps.publication

 }            

#============= Definition of CORDEX specific test functions ===================================

