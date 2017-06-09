# -*- coding: utf-8 -*-
"""

Form handling workflow definitions
===================================

workflow steps are characterized by dictionaries

workflow entities are characterized according to the W3C PROV model

* ENTITIES defining the input or output of workflow steps
* AGENTS defining the persons (or tools) responsible for the workflow steps
* ACTIVITEIS defining the execution progress and status of workflow steps

The definitions in this configuration are generic, and thus can be applied to all FormFabric supported projects


@author: stephan

ToDo: Merge with variable tests ...
"""
# name spaces for w3c prov transformation of submission provenance information

workflow_steps_version = "1.0"

NAME_SPACES={'sub':'http://enes.org/entities/ingest-workflow#',
             'ing':'http://enes.org/entities/ingest-workflow#',
             'qua':'http://enes.org/entities/ingest-workflow#',
             'pub':'http://enes.org/entities/ingest-workflow#',        
             'wf':'http://enes.org/entities/ingest-workflow#',        
             'dm':'http://enes.org/entities/ingest-workflow#',        
             'dp':'http://enes.org/entities/ingest-workflow#',        
             'node':'http://enes.org/entities/ingest-workflow#',        
            }

            

# -------------------------------------------------------------------------------------------------------------------------
# workflow step: data submission
SUBMISSION_AGENT = { 
             '__doc__': """Attributes characterizing the person responsible for form completion and submission:
            
                                   - last_name: Last name of the person responsible for the submission form content
                                   - first_name: Corresponding first name
                                   - email: Valid user email address: all follow up activities will use this email to contact end user
                                   - key_word : user provided key word to remember and separate submission
                             """,
              'i_name': 'submission_agent',               
              'last_name' : '',
              'first_name' : '',
              'key_word': '',
              'email': ''}
             

SUBMISSION_ACTIVITY = {
          '__doc__': """
                         Attributes characterizing the form submission activity:
                         
                         - submission_comment : free text comment
                         - submission_method  : How the submission was generated and submitted to DKRZ: email or DKRZ form server based       
                         """,
           'i_name':'submission_activity',              
           'submission_comment':'',
           'submission_method':'',
           'pwd':' password to access form '
            } 
       
            
SUBMISSION_FORMTEMPLATE_ENTITY = {
            '__doc__' : """
                           Attributes defining the form template used:
                               
                               - source_path: path to the form template used (jupyter notebook)         
                               - form_template_version:  version string for the form template used
                               - tag: git tag of repo containing templates (=source code repo in most cases)
                """,
             'i_name': 'submission_form_template_entity',   
             'source_path' : '', # filled with path of original template form      
             'form_template_version': '', # version of form template / form tool
             'tag': '' # git tag
            }

SUBMISSION_FORM_ENTITY = {
            '__doc__': """
                     Attributes characterizing the form submission process and context:
                     - form: Form object for all end user provided information
                     - form_name: consistent prefix for the form name (postfix=.ipynb and .json)
                     - form_repo: git repo where forms are stored (before submission)
                     - form_json, form_repo_path: full paths to json and ipynb representations
                     - form_dir: directory where form are served to the notebook interface
                     - status: status information
                     - checks_done: form consistency checks done
                     - tag: 'git tag of submission form in submission form repo',
                     - repo: '(gitlab) repo where the tag relates to','
                     
                   """,
            'i_name': 'submission_form_entity',       
            'form': '',       
            'form_name': '',
            'form_repo' :'',          
            'form_json': '',
            'form_path': '',
            'form_repo_path' : '',
            'form_dir': '',
            'status': '',
            'checks_done' : '',
            'tag': '',
            'repo': '',
            'form_info': {}
}            
                                 

DATA_SUBMISSION = {
     '__doc__': """ 
           Attributes characterizing the data submission workflow step:
           - entity_in : Input (form template and init info)
           - entity_out: Output (submission form information)
           - agent: person or tool related information
           - activity': submission activity related information
           """,
     'i_name':'data_submission',      
     'entity_in': SUBMISSION_FORMTEMPLATE_ENTITY,
     'entity_out': SUBMISSION_FORM_ENTITY,
     'agent': SUBMISSION_AGENT,
     'activity': SUBMISSION_ACTIVITY
}

# 
#---------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# workfow step: submission review
#


REVIEW_AGENT =  {  
            '__doc__':""" 
                   Attributes characterizing the person or tool checking the form:
                    - responsible_person:  
                    """,
            'i_name':'review_agent',         
            'responsible_person': ""
            }
                                   
            
REVIEW_ACTIVITY =  {
       '__doc__': """
           Attributes characterizing the form review activity:
            - ticket_url: assigned RT Ticket
            - ticket_id: RT Ticket id 
            - review_comment: free text comment 
            - review_status: progress status of review
            - review_report: dictionary with review results and issues
        """,
            'i_name':'review_activity',
            'review_comment': '',
            'ticket_url':'',
            'ticket_id' :0,
            'review_status':'',
           }


REVIEW_REPORT = {
     '__doc__': """
         Attributes characterizing the review results:
         - data: time stamp of last results
         - tag: git tag for repo conatining report information
         - repo: (gitlab) repo containing report information,
         - comment: free text comment for this review,
         - status : review status information: ok, undef, uncomplete, error,
         - form_info: report details in dictionary   
     """,
     'i_name':'review_report',
     'date': '',
     'tag' : '',
     'repo': '',
     'comment' : '',
     'status' : '',
     'dict': ''
} 
 
DATA_SUBMISSION_REVIEW = {
     '__doc__': """ 
           Attributes characterizing the data submission review step:
           - entity_in :  submission form
           - entity_out: adapted submission form
           - agent: person or tool related information
           - activity': submission activity related information
           """,
    'i_name': 'data_submission_review',       
    'entity_in': SUBMISSION_FORM_ENTITY,
    'entity_out': REVIEW_REPORT,
    'agent': REVIEW_AGENT, 
    'activity': REVIEW_ACTIVITY
    }

#    
#-------------------------------------------------------------------------------------------------------- 

#--------------------------------------------------------------------------------------------------------
# workflow step: data ingest            


INGEST_AGENT = {
                '__doc__':""" 
                   Attributes characterizing the person or tool managing the data ingest:
                    - responsible_person:  
                    """,
                'i_name':'ingest_agent',    
                "responsible_person": "",
                }
              

INGEST_ACTIVITY = {
    '__doc__': """
        Attributes characterizing the data ingest activity:
        - status: status information
        - timestamp_started
        - timestamp_finished : data ingest timing information
        - comment : free text comment
        - ticket_id: related RT ticket number
        - ingest_report: dictionary with ingest related information (tbd.)
        """,
     "i_name":'ingest_activity',   
     "status": "", 
     "timestamp_started":"",
     "timestamp_finished":"",
     "comment":"", 
     "ticket_id": 0,
     "ingest_report": {}         
}   
            

INGEST_REPORT = {
     '__doc__': """
     Attributes characterizing the ingest report summary:
       - date: 'last modification date,
       - tag : '(git) tag for repo containing report information,
       - repo: '(gitlab) repo containing report information,
       - comment : 'free text comment for this review,
       - status : 'data ingest status information: ok, undef, uncomplete, error,
       - form_info: 'report details in dictionary,
     """,
     'i_name':'ingest_report',
     'date': '',
     'tag' : '',
     'repo': '',
     'comment' : '',
     'status' : '',
     'form_info': ''
}


DATA_INGEST = {
    '__doc__': """
       Attributes characterizing the data ingest workflow step:
       - entity_in : data review report
       - entity_out : data ingest report
       - agent : person or tool related ingest step information 
       - activity : information on the ingest process
       """,
    'i_name':'data_ingest',
    'entity_in': REVIEW_REPORT,
    'entity_out': INGEST_REPORT,
    'agent': INGEST_AGENT, 
    'activity': INGEST_ACTIVITY
    }       
# 
#----------------------------------------------------------------------------------------------------- 


#-----------------------------------------------------------------------------------------------------         
# workflow step: data quality assurance
#             
             
QUA_AGENT = {
            '__doc__':""" 
                   Attributes characterizing the person or tool managing the data ingest:
                    - responsible_person:  
                    """,
             'i_name':'qua_agent',       
             "responsible_person": ""
             }              

QUA_ACTIVITY= {
    '__doc__': """
        Attributes characterizing the data quality assurance activity:
        - status: status information
        - timestamp_started
        - timestamp_finished : data ingest timing information
        - comment : free text comment
        - ticket_id: related RT ticket number
        - follow_up_ticket: in case new data has to be provided
        - quality_report: dictionary with quality related information (tbd.)
        """,
      'i_name':'qua_activity',  
      "status": "",
      "timestamp_started":"",
      "timestamp_finished":"",
      "comment":"",      
      "ticket_id": "",
      "follow_up_ticket": '', # qa feedback to users, follow up actions
             }
              
    
QUA_REPORT = {
   '__doc__': """
     Attributes characterizing the quality report summary:
       - date: 'last modification date,
       - tag : '(git) tag for repo containing report information,
       - repo: '(gitlab) repo containing report information,
       - comment : 'free text comment for this review,
       - status : 'data ingest status information: ok, undef, uncomplete, error,
       - form_info: 'report details in dictionary   
     """,
     'i_name':'qua_report',
     'date': '',
     'tag' : '',
     'repo': '',
     'comment' : '',
     'status' : '',
     'form_info': ''      
    }

    
DATA_QUALITY_ASSURANCE = {
    '__doc__': """
        Attributes characterizing the data quality assurance step:
        - entity_in: data ingest report
        - entity_out:  data quality assurance report
        - agent: person and tool responsible for qua checking
        - activity: info on qua checking process
    """,
    'i_name':'data_quality_assurance',
    'entity_in': INGEST_REPORT,
    'entity_out': QUA_REPORT,
    'agent': QUA_AGENT, 
    'activity': QUA_ACTIVITY
    }

#
#-------------------------------------------------------------------------------------------
# workflow step: data publication  
#           -              
             

PUBLICATION_AGENT = {
     '__doc__': """
        Attributes characterizing the persons performing the data publication:
         - responsible_person: person name
         - publication_tool: string characterizing the publication tool
     """,
    'i_name':'publication_agent', 
    "responsible_person": "",
    'publication_tool':""
 }


PUBLICATION_ACTIVITY =  {
     '__doc__': """ Attributes characterizing the data publication activity:
        - status: status information
        - timestamp_started
        - timestamp_finished : data ingest timing information
        - comment : free text comment
        - ticket_id: related RT ticket number
        - follow_up_ticket: in case new data has to be provided
        """,
      'i_name':'publication_activity',  
      "status": "",
      'timestamp_started':"",
      'timestamp_finished':"",
      "comment": "",
      "ticket_id": "", 
      'follow_up_ticket':""
           }
             
PUBLICATION_REPORT = {
            '__doc__':""" 
               Attributes characterizing the data publication report
               - date: last modification date,
               - tag : (git) tag for repo containing report information,
               - repo: (gitlab) repo containing report information,
               - comment : free text comment for this review,
               - status : data ingest status information: ok, undef, uncomplete, error,
               - form_info: 'report details in dictionary
             """,
            'i_name':'publication_report', 
            'date': '',
            'tag' : '',
            'repo': '',
            'comment' : '',
            'status' : '',
            'form_info': '',
            'facet_string': "# e.g. project=A&model=B& ...."
             }            


DATA_PUBLICATION = {
    '__doc__':"""
        Attributes characterizing the data publication workflow step:
        - entity_in: 
        - entity_out:
        - agent:
        - activity:
     """,
    'i_name': 'data_publication', 
    'entity_in': QUA_REPORT,
    'entity_out': PUBLICATION_REPORT,
    'agent': PUBLICATION_AGENT, 
    'activity': PUBLICATION_ACTIVITY
    }

#
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# workflow step: data archival (and DOI assignment for data citation)
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

#
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# summary dict for workflow steps known to the system
# 

WORKFLOW_DICT = {
     'data_submission': DATA_SUBMISSION, 
     'data_submission_review': DATA_SUBMISSION_REVIEW, 
     'data_ingest': DATA_INGEST, 
     'data_quality_assurance': DATA_QUALITY_ASSURANCE,
     'data_publication': DATA_PUBLICATION,
    # 'data_archival': DATA_PRESERVATION 
     }
      
#
#---------------------------------------------------------------------------------------------------
