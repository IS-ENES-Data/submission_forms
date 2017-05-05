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

# keystore_path is set to join(FORM_REPO,keystore) 

FORM_REPO = "/home/stephan/tmp/Repos/form_repo"

# final submissions repo (gitlab synchronized)
SUBMISSION_REPO = "/home/stephan/tmp/Repos/submission_repo"

rt_pwd = base64.b64decode("Y2Y3RHI2dlM=")
#print project_directory
#print "general project config imported"

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
             "workflow": [("sub","data_submission"),
                       #   ("rev","data_submission_review"),
                       #   ("ing","data_ingest"),
                       #   ("qua","data_quality_assurance"),
                       #   ("pub","data_publication"),
                       #   ("da", "data_archival")
                         ], 
             }
                         

generic_dict = {
             "first_name":""
             }
             
# to do: put generic info in generic_dict and merge this with 
#        the project_dicts below
PROJECT_DICT['DKRZ_CDP'] = {
             'project': 'CMIP6_CDP',
             "workflow": [("sub","data_submission"),
                          ("rev","data_submission_review"),
                          ("ing","data_ingest"),
                          ("qua","data_quality_assurance"),
                          ("pub","data_publication"),
                          ("da", "data_archival")
                         ], 
 }
PROJECT_DICT['test'] = {
             '__doc__' :"""
             Form object for project test
            
             Workflow step related sub-forms (filled by data managers):
               - sub: data submission form
               - rev: data review_form
               - ing: data ingest form
               - qua: data quality assurance form
               - pub: data publication form
               
            
             
             Each workfow step form is structured according to
               - entity_in : input information for this step
               - entity_out: output information for this step
               - agent: information related to responsible party for this step
               - activity: information related the workflow step execution
               
              End user provided form information is stored in:
             
             _this_form_object.sub.entity_out.form  
             
             The following end user attributes are defined:
           
               - project: project this form is related to
               - ....
               
             """ ,
             'project':'test',
             "workflow": [("sub","data_submission"),
                          ("rev","data_submission_review"),
                          ("ing","data_ingest"),
                          ("qua","data_quality_assurance"),
                      #    ("pub","data_publication"),
                      #    ("da", "data_archival")
                         ], 
 }
PROJECT_DICT['CMIP6']= {
             'project' : 'CMIP6',
            "workflow": [("sub","data_submission"),
                          ("rev","data_submission_review"),
                          ("ing","data_ingest"),
                          ("qua","data_quality_assurance"),
                          ("pub","data_publication"),
                          ("da", "data_archival")
                         ], 
 }            
 
PROJECT_DICT['ESGF_replication']= {
             'project' : 'CMIP6_replication',
             "workflow": [("sub","data_submission"),
                          ("rev","data_submission_review"),
                          ("ing","data_ingest"),
                          ("qua","data_quality_assurance"),
                          ("pub","data_publication"),
                          ("da", "data_archival")
                         ], 
 }            

#============= Definition of CORDEX specific test functions ===================================

