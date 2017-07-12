# -*- coding: utf-8 -*-
"""

Project dictionaries
======================

The dictionaries defining the keywords for the individual projects are defined here.
They get accessible to the FormFabric code by adding them to the PROJECT_DICT dictionary.

Thus e.g. PROJECT_DICT['CMIP6'] defines to the overall keyword dictionary used for CMIP6 data
     e.g. PROJECT_DICT['CMIP6_FORM'] defines the keyword (sub-)dictionary with the information from the data providers
                                     (by filling the jupyter notebook based FORMs)

To define the data management steps used in the individual projects, the 'workflow' keyword is used.

Thus e.g. PROJECT_DICT['CMIP6']['workflow'] provides the list (of lists) defining the workflow steps.

The workflow steps are defined in .ref workflow_steps.py

@author: stephan


.. automodule:: dkrz_forms.config.settings
.. automodule:: dkrz_forms.config.workflow_steps

"""

#================================================================================================
# This first section should stay as it is .. make project specific extensions in the second part
# 

# name spaces for w3c prov transformation of submission provenance information

import base64
from string import Template


rt_pwd = base64.b64decode("Y2Y3RHI2dlM=")

# End of first part
#================================================================================================


#================================================================================================
# Second section: definition of project dictionaries
# 

PROJECT_DICT = {}

PROJECTS = ['CORDEX','CMIP6','test','ESGF_replication','DKRZ_CDP']


generic_wflow_description = Template("""
        Form object for project $project
            
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
               
              End user provided form information is stored in
                _this_form_object.sub.entity_out.form  
             
             The following generic attributes are defined:
           
               - project: project this form is related to
               - workflow: the workflow steps which are defined for this project
               - status: overall workflow status 
                   (keyword-structure = "workflow_step"_start, "workflow_step"_end
                   e.g. sub_start, sub_end
               """)

for project in PROJECTS:
# submitted information
    PROJECT_DICT[project]  = {
          '__doc__': generic_wflow_description.substitute(project=project),
          "project":project,        
          "workflow": [("sub","data_submission"),
                       ("rev","data_submission_review"),
                       ("ing","data_ingest"),
                       ("qua","data_quality_assurance"),
                       ("pub","data_publication"),
                      # ("da", "data_archival")
           ],
          "status":  "sub_start"           
            }  

PROJECT_DICT['CORDEX_FORM'] = {
             "__doc__":"""
                         CORDEX information collected as part of form completion process
                         see CORDEX template
                         .. details on entries .. to be completed
                        """,
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
             "uniqueness_of_tracking_id" : ""}                         


PROJECT_DICT['DKRZ_CDP_FORM'] = {
            "__doc__":"""
                 DKRZ CMIP Data pool ingest request related informtion .. to be completed 
             """,
             "project":"DKRZ_CDP",
             "comment": ""
             }

PROJECT_DICT['CMIP6_FORM'] = {
            "__doc__":"""
                 DKRZ CMIP6 data ingest and publication request information  .. to be completed 
             """,
             "project":"CMIP6",
             "comment": ""
            }

PROJECT_DICT['test_FORM'] = {
            "__doc__":"""
                 test request related informtion .. to be completed 
             """,
             "project":"test",
             "comment": ""
}

PROJECT_DICT['ESGF_replication_FORM'] = { 
            "__doc__":"""
                 ESGF replication request related informtion .. to be completed 
             """,
             "project":"ESGF_replication",
             "comment": ""
            }


#           
# End of section two
#================================================================================

