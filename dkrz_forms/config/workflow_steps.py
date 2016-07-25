# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:11:02 2016

@author: stephan

ToDo: Merge with variable tests ...
"""

# the following workflow steps are defined based on CVs:
# - submission and review
# - ingest 
# - quality assurance
# - publication
# - archival 
# all workflow steps are structured according to the W3C Prov model
# thus they define an agent, activity and input/output artefacts 



# name spaces for w3c prov transformation of submission provenance information
name_space={'sub':'http://enes.org/entities/ingest-workflow#',
            'ing':'http://enes.org/entities/ingest-workflow#',
            'che':'http://enes.org/entities/ingest-workflow#',
            'pub':'http://enes.org/entities/ingest-workflow# '        
            }
            


#### submission + review CV  --- separated into sections appropriate for PROV representation 
submission_agent = { 
              'last_name' : '',
              'first_name' : '',
              'keyword': '',
              'email': ''}

submission_activity = {
           'submission_comment':'',    # addition info given by the submission_agent (e.g.received by separate email etc.)
           'submission_method':'',     # CV: tbd, e.g. DKRZ_online_form, email, ..
           'id': '',                   # automatically generated identifier as part of form creation
           'commit_hash': '',          # automatically generated git hash of storing submission form locally 
           'substatus': ''
            } 
            
submission_form_template = {
             'workflow_steps_version' : "1.0",
             'source_path' : '', # filled with path of original template form      
             'form_version': '', # version of form template / form tool 
            }
             
submission_form_filled = {
            'form_name': '',       # project_lastname_keyword
            'subform_path' :'',    # full path to ipython notebook form
            'form_path': '',       # full directory path to ipython notebook
            'package_name':'',     # json package name 
            'package_path': '',    # json package full path
            'repo': '',            # proect directory (part of config)
            'checks_done' : "none" # status of form checks
            }

# ---------------------------------------------------------------------------------------------------
 
review_agent =  {        
            'responsible_person': ""
            }
            
review_activity =  {
            'review_comment': '',
            'ticket_url':'',
            'ticket_id' : 0,
            'timestamp' : ""
           }

review_report = {
          'report_ticket_subject':'', # subject of ticket describing review 
                                     # --> to do: ticket subject conventions for data managers
          'review_summary': ''
              }          
# ------------------------------------------------------------------------------------------------------
submit_part = {}
submit_part.update(submission_agent)
submit_part.update(submission_activity)
submit_part.update(submission_form_template)
submit_part.update(submission_form_filled)

review_part = {}
review_part.update(review_activity)
review_part.update(review_report)
     
submission = {}
submission.update(submit_part)
submission.update(review_part)
             

# 2. step: information related to data ingest phase             
#          - associated rt ticket(s) or ticket comments
#          - target directory (input for QA step)
#          - ..
# 


ingest_agent = {
                "responsible_person": "",
                }

ingest_activity = {
             "status": "", 
             "timestamp_started":"",
             "timestamp_finished":"",
             "comment":"", 
             "ticket_id": "",
         
             }   
 
ingest_report =     {
             "drsdir_file_pattern": "", #glob file pattern for ingested data
             "target_directory": "",
               }  
               
               
data_ingest = {}
data_ingest.update(ingest_agent)  
data_ingest.update(ingest_activity)  
data_ingest.update(ingest_report)           
# 3. step: information related to data quality assurance phase:
#             - ----            
             
qua_agent = {
             "responsible_person": "",

             }

qua_activity = {
             "status": "",
             "timestamp_started":"",
             "timestamp_finished":"",
             "comment":"",      
             "ticket_id": "",
             "follow_up_ticket": '', # qa feedback to users, follow up actions
             }

qua_report = {
             "target_directory": "", # qa reports
             "qua_status":"",
             "qua_comment":"",
             "qa_tool_version": '',
            }

qua = {}
qua.update(qua_agent)
qua.update(qua_activity)
qua.update(qua_report)
# 4. step: information related to ESGF publication phase  
#           -              
             
pub_agent = {
            "responsible_person": "",
           }

pub_activity =  {
           "status": "",
           "comment": "",
           "timestamp": "",
           "ticket_id": "", 
           }

pub_report = {
             "pid_collections" : "",
             "publish_date": "",
             "search_string" : "", # cog url including facet search string
             "facet_string": "", # e.g. project=A&model=B& ....
             }


publication = {}
publication.update(pub_agent)
publication.update(pub_activity) 
publication.update(pub_report)       
# submitted information
#cordex_dict  = {
#             "first_name": "",
#             "last_name" : "",
#             "email" : "",
#             "submission_type" : "",
#             "institution" : "",
#             "institute_id" : "",
#             "model_id" : "",
#             "experiment_id" : "",
#             "time_period" : "",
#             "example_file_name" : "",
#             "grid_mapping_name" : "",
#             "grid_as_specified_if_rotated_pole" : "",
#             "data_qc_status" : "",
#             "data_qc_comment" : "",
#             "terms_of_use" : "",
#             "directory_structure" : "",
#             "data_path" : "",
#             "data_information" : "",
#             "exclude_variables_list" : "",
#             "variable_list_day" : "",
#             "variable_list_mon" : "",
#             "variable_list_sem" : "",
#             "variable_list_fx" : "",
#             "uniqueness_of_tracking_id" : "",
#             'sub': submission,
#             'ing': data_ingest,
#             'che':qua,
#             'pub':publication
#             
#             }
 

#============= Definition of CORDEX specific test functions ===================================

