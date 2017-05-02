# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:11:02 2016

@author: stephan

ToDo: Merge with variable tests ...
"""
# name spaces for w3c prov transformation of submission provenance information

workflow_steps_version = "1.0"

NAME_SPACES={'sub':'http://enes.org/entities/ingest-workflow#',
            'ing':'http://enes.org/entities/ingest-workflow#',
            'che':'http://enes.org/entities/ingest-workflow#',
            'pub':'http://enes.org/entities/ingest-workflow# '        
            }
            
            # 1.step: information related to submission management phase
#         - associated rt tickets
#         - associated git commit(s)
#         - associated check status 
#         - ....    

# Specify the workflow steps in a List
# for each step in workflow specifiy the W3C prov components:
# -- entities (input, output)
# -- activities (transforming input to output)
# -- agents (persons, SW engaged in activities)


# data submission
SUBMISSION_AGENT = { 
              'last_name' : '',
              'first_name' : '',
              'key_word': '',
              'email': ''}
              
SUBMISSION_AGENT_DOC = {
              'last_name' : 'Last name of the person responsible for the submission form content',
              'first_name' : 'Correstponding first name',
              'key_word': 'A user provided key word to remember the submission form',
              'email': 'Valid user email address: all follow up activities will use this email to contact end user',
              'doc_string': """Attributes characterizing the person responsible for form completion and submission:
              
                                   - last_name
                                   - first_name
                                   - email
                                   - key_word : user provided key word to remember and separate submission
                             """
                             }             

SUBMISSION_ACTIVITY = {
           'submission_comment':'',
           'submission_method':''           
            } 
            
SUBMISSION_ACTIVITY_DOC = {
           'submission_comment':'a free text comment for this submission',
           'submission_method':"""
                  How the submission was generated and submitted to DKRZ: 
                     'email' or 'formserver' 
                     """,
           'doc_string': """
                         Attributes characterizing the form submission activity:
                         
                         - submission_comment : free text comment
                         - submission_method  : email or DKRZ form server based       
                         """
}            
            
SUBMISSION_FORMTEMPLATE_ENTITY = {
             'source_path' : '', # filled with path of original template form      
             'form_version': '', # version of form template / form tool 
            }
            
SUBMISSION_FORMTEMPLATE_ENTITY_DOC = { 
            'source_path' : "path to the form template used (jupyter notebook)",
            'form_version' : "version string for the form template used",                          
            'doc_string' : """
                           Attributes defining the form template used:
                               
                               - source_path         
                               - form_version 

                           """                
}

SUBMISSION_FORM_ENTITY = {
            'form_name': 'Naming pattern of the form: project_name+_+last_name+_+keyword',
            'form_repo' :'(git) directory where stored forms are maintained',          
            'form_json': 'full path to json representation of the form',
            'form_repo_path' : 'full path to notebook representation of the form',
            'form_dir': 'directoy where forms are served and (temporarily) stored',
            'status': 'status information of form',
            'checks_done' : 'consistency checks done for this form',
            'doc_string': """
                     Attributes characterizing the form submission process and context:
                     - form_name: consistent prefix for the form name (postfix=.ipynb and .json)
                     - form_repo: git repo where forms are stored (before submission)
                     - form_json, form_repo_path: full paths to json and ipynb representations
                     - form_dir: directory where form are served to the notebook interface
                     - status: status information
                     - checks_done: form consistency checks done
                     . ...
                     
    
                   """ 
}            
                         
SUBMISSION_FORM_ENTITY_DOC = {
            'form_name': 'Naming pattern of the form: project_name+_+last_name+_+keyword',
            'form_repo' :'(git) directory where stored forms are maintained',          
            'form_json': 'full path to json representation of the form',
            'form_repo_path' : 'full path to notebook representation of the form',
            'form_dir': 'directoy where forms are served and (temporarily) stored',
            'status': 'status information of form',
            'checks_done' : 'consistency checks done for this form',
            'doc_string': """
                     Attributes characterizing the form submission process and context:
                     - form_name: consistent prefix for the form name (postfix=.ipynb and .json)
                     - form_repo: git repo where forms are stored (before submission)
                     - form_json, form_repo_path: full paths to json and ipynb representations
                     - form_dir: directory where form are served to the notebook interface
                     - status: status information
                     - checks_done: form consistency checks done
                     . ...
                     
    
                   """ 
}            

DATA_SUBMISSION = {
     'entity_in': SUBMISSION_FORMTEMPLATE_ENTITY,
     'entity_out': SUBMISSION_FORM_ENTITY,
     'agent': SUBMISSION_AGENT,
     'activity': SUBMISSION_ACTIVITY
}

DATA_SUBMISSION_DOC = {
     'entity_in': SUBMISSION_FORMTEMPLATE_ENTITY_DOC,
     'entity_out': SUBMISSION_FORM_ENTITY_DOC,
     'agent': SUBMISSION_AGENT_DOC,
     'activity': SUBMISSION_ACTIVITY_DOC
}


#  data review
 
REVIEW_AGENT =  {        
            'responsible_person': ""
            }
            
REVIEW_ACTIVITY =  {
            'review_comment': '',
            'ticket_url':'',
            'ticket_id' : 0,
           }

REVIEW_REPORT = {
          'report_ticket_subject':'', # subject of ticket describing review 
                                     # --> to do: ticket subject conventions for data managers
          'review_summary': ''
              } 
 
DATA_SUBMISSION_REVIEW = {
    'entity_in': SUBMISSION_FORM_ENTITY,
    'entity_out': REVIEW_REPORT,
    'agent': REVIEW_AGENT, 
    'activity': REVIEW_ACTIVITY
    }
     
             

# 2. step: information related to data ingest phase             
#          - associated rt ticket(s) or ticket comments
#          - target directory (input for QA step)
#          - ..
# 


INGEST_AGENT = {
                "responsible_person": "",
                }

INGEST_ACTIVITY = {
             "status": "", 
             "timestamp_started":"",
             "timestamp_finished":"",
             "comment":"", 
             "ticket_id": "",
         
             }   
 
INGEST_REPORT =     {
             "drsdir_file_pattern": "", #glob file pattern for ingested data
             "target_directory": "",
               }  
               

DATA_INGEST = {
    'entitiy_in': SUBMISSION_FORM_ENTITY,
    'entity_out': SUBMISSION_FORM_ENTITY,
    'agent': INGEST_AGENT, 
    'activity': INGEST_ACTIVITY
    }
          
# 3. step: information related to data quality assurance phase:
#             - ----            
             
QUA_AGENT = {
             "responsible_person": "",
             }

QUA_ACTIVITY= {
             "status": "",
             "timestamp_started":"",
             "timestamp_finished":"",
             "comment":"",      
             "ticket_id": "",
             "follow_up_ticket": '', # qa feedback to users, follow up actions
             }

QUA_REPORT_ENTITY = {
             "target_directory": "", # qa reports
             "qua_status":"",
             "qua_comment":"",
             "qa_tool_version": '',
            }

DATA_QUALITY_ASSURANCE = {
    'entity_in': SUBMISSION_FORM_ENTITY,
    'entity_out': SUBMISSION_FORM_ENTITY,
    'agent': QUA_AGENT, 
    'activity': QUA_ACTIVITY
    }

# 4. step: information related to ESGF publication phase  
#           -              
             
PUBLICATION_AGENT = {
            "responsible_person": "",
           }

PUBLICATION_ACTIVITY =  {
           "status": "",
           "comment": "",
           "timestamp": "",
           "ticket_id": "", 
           }

PUBLICATION_REPORT_ENTITY = {
             "pid_collections" : "",
             "publish_date": "",
             "search_string" : "", # cog url including facet search string
             "facet_string": "", # e.g. project=A&model=B& ....
             }


DATA_PUBLICATION = {
    'entity_in': SUBMISSION_FORM_ENTITY,
    'entity_out': SUBMISSION_FORM_ENTITY,
    'agent': PUBLICATION_AGENT, 
    'activity': PUBLICATION_ACTIVITY
    }

# 5. step: information related to archival, preservation and DOI assignment
# 

PRESERVATION_AGENT = {
            "responsible_person": "",
           }

PRESERVATION_ACTIVITY =  {
           "status": "",
           "comment": "",
           "timestamp": "",
           "ticket_id": "", 
           }

PRESERVATION_REPORT_ENTITY = {
             "pid_collections" : "",
             "publish_date": "",
             "search_string" : "", # cog url including facet search string
             "facet_string": "", # e.g. project=A&model=B& ....
             }


DATA_PRESERVATION = {
    'entities_in': SUBMISSION_FORM_ENTITY,
    'entities out': SUBMISSION_FORM_ENTITY,
    'agent': PRESERVATION_AGENT, 
    'activity': PRESERVATION_ACTIVITY
    }

#=============================================================================
WORKFLOW_DICT = {
     'data_submission': DATA_SUBMISSION, 
     'data_submission_review': DATA_SUBMISSION_REVIEW, 
     'data_ingest': DATA_INGEST, 
     'data_quality_assurance': DATA_QUALITY_ASSURANCE,
     'data_publication': DATA_PUBLICATION,
     'data_archival': DATA_PRESERVATION }
      
DOCUMENTATION_DICT = {
     'data_submission': DATA_SUBMISSION_DOC }

#DOCUMENTATION_DICT['data_submission'] = DATA_SUBMISSION_DOC


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

