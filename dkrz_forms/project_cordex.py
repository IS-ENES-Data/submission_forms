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
            'status': 'filling', #  filling -> stored -> ready -> submitted / submission_error 
            'last_name' : '',
            'first_name' : '',
            'key_word': '',
            'email': '',
            'form_name': '',
            'form_path: '',
            'package_name':'', # json package
            'package_path': '', 
            'repo': '',
            'ticket_id' : 0,
            'checks_done' : "none",
            'timestamp' : "",
            'id': '',
            'source_path' : '', # filled with path of original template form
            'responsible_person': "",
            'form_version': '' # version of form template / form tool
            'ticket_id':'',
            'ticket_url':'',
            'comment': '', 
            }

# 2. step: information related to data ingest phase             
#          - associated rt ticket(s) or ticket comments
#          - target directory (input for QA step)
#          - ..
# 

ingest = {
             "status": "", 
             "timestamp_started":"",
             "timestamp_finished":"",
             "comment":"", 
             "target_directory": "",
             "ticket_id": ""
             "responsible_person",
             "dir_file_pattern": "", #glob file pattern for ingested data
             }   
             
# 3. step: information related to data quality assurance phase:
#             - ----            
             
quality_assurance = {
             "status": "",
             "timestamp_started":"",
             "timestamp_finished":"",
             "comment":"", 
             "target_directory": "", # qa reports
             "ticket_id": "",
             "responsible_person": '',
             "qa_tool_version": '',
             "follow_up_ticket": '', # qa feedback to users, follow up actions
             }


# 4. step: information related to ESGF publication phase  
#           -              
             
publication = {
             "status": "",
             "comment": "",
             "timestamp": "",
             "search_string" : "", # cog url including facet search string
             "ticket_id": "", 
             "facet_string": "", # e.g. project=A&model=B& ....
             "pid_collections" = ""
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

