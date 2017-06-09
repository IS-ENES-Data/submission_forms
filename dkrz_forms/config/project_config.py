# -*- coding: utf-8 -*-
"""

Project dictionaries
======================

The dictionaries defining the keywords for the individual projects are defined here.
They get accessible to the FormFabric code by adding them to the PROJECT_DICT dictionary.

Thus e.g. PROJECT_DICT['CMIP6'] refers to the keyword dictionary used for CMIP6 data

To define the data management steps used in the individual projects, the 'workflow' keyword is used.

Thus e.g. PROJECT_DICT['CMIP6']['workflow'] provides the list (of lists) defining the workflow steps.

The workflow steps are defined in .ref workflow_steps.py

@author: stephan


.. automodule:: dkrz_forms.config.settings
.. automodule:: dkrz_forms.config.workflow_steps

ToDo: 

* Merge with variable tests ...
* refine NAME_SPACE definitions (later move e.g. to a separate W3C prov handling package

"""

#================================================================================================
# This first section should stay as it is .. make project specific extensions in the second part
# 

# name spaces for w3c prov transformation of submission provenance information
from os.path import join as join
import base64



rt_pwd = base64.b64decode("Y2Y3RHI2dlM=")

# End of first part
#================================================================================================


#================================================================================================
# Second section: definition of project dictionaries
# 

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
                          ("rev","data_submission_review"),
                          ("ing","data_ingest"),
                          ("qua","data_quality_assurance"),
                          ("pub","data_publication"),
                          ("da", "data_archival")
                         ], 
             }
                         

PROJECT_DICT['DKRZ_CDP'] = {
             '__doc__': """
             Form object for data replication related information
             
             Workflow steps related sub-forms (filled by data manager):
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
             
             The the documentation of the sub.entity_out subform for 
             the end-user filled information entities 
             """,
             'project': 'CMIP6_CDP',
             "workflow": [("sub","data_submission"),
                          ("rev","data_submission_review"),
                          ("ing","data_ingest"),
                          ("qua","data_quality_assurance"),
                          ("pub","data_publication"),
#                          ("da", "data_archival")
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
                          ("pub","data_publication"),
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
#                          ("da", "data_archival")
                         ], 
 }            
 
PROJECT_DICT['ESGF_replication']= {
             'project' : 'CMIP6_replication',
             "workflow": [("sub","data_submission"),
                          ("rev","data_submission_review"),
                          ("ing","data_ingest"),
                          ("qua","data_quality_assurance"),
                          ("pub","data_publication"),
#                          ("da", "data_archival")
                         ], 
 } 

#           
# End of section two
#================================================================================

