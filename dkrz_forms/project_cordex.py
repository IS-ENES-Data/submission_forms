# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:11:02 2016

@author: stephan

ToDo: Merge with variable tests ...
"""
# name spaces for w3c prov transformation of submission provenance information
name_space={'sub':'http://enes.org/entities/ingest-workflow#',
            'ing':'http://enes.org/entities/ingest-workflow#',
            'che':'http://enes.org/entities/ingest-workflow#',
            'pub':'http://enes.org/entities/ingest-workflow# '        
            }
            
            # 1.step: information related to submission management phase
#         - associated rt tickets
#         - associated git commit(s)
#         - associated check status 
#         - ....    

        
submission = {
             "timestamp": "",
             'responsible_person' : "pl",
             "repo": "",
             "check_status" :"not checked",
             "package_path" :"",
             "package_name" :"",
             "ticket_id" :"",
             "status" :"initial",
             "form_name":""
             }

# 2. step: information related to data ingest phase             
#          - associated rt ticket(s) or ticket comments
#          - target directory (input for QA step)
#          - ..
# 

ingest = {
             'responsible_person' : "pl",
             "target_directory": "",
             "ticket_id": ""
             }   
             
# 3. step: information related to data quality assurance phase:
#             - ----            
             
quality_assurance = {
             'responsible_person' : "hdh",
             "status": "",
             "ticket_id": "",
             "report_dir": ""
             }
# 4. step: information related to ESGF publication phase  
#           -              
             
publication = {
             'responsible_person' : "kb",
             "status": "",
             "ticket_id": "", 
             "facet_search_string": ""
}             

         

# submitted information
cordex_dict  = {
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
             'sub': submission,
             'ing': ingest,
             'che':quality_assurance,
             'pup':publication
             
             }
 

#============= Definition of CORDEX specific test functions ===================================

