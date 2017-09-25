from six import string_types
import re

from dkrz_forms import utils,config 
from IPython.display import display
# from IPython.core.display import HTML
# from collections import OrderedDict

def check_email(email):
    if re.match(""r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email) != None:
       return 1
    else: 
       return 0


## ToDo: if necessary, parts could be implemented based on abstract schema mechanisms like json schema
##       yet for the time being this is probably enough for a quick data conformance check ...

def get_options(mystring):
    ''' convert a comma separated string to a list
    '''
    result = list(map(str.strip, mystring.split(',')))
    if len(result)==1:
        return [""]
    else:
        return result

def check_cv(my_string,template_string):
    print("Vocalbulary test:", template_string)
    return(1, "CV check not yet implemented")

def check_valid_string(key, my_string,template_string):
    if isinstance(my_string, string_types) and isinstance(template_string, string_types): 
        
        
        if template_string.startswith("CV"):
            return check_cv(my_string,template_string)
        
        if template_string.startswith("mandatory"):
            if my_string == template_string:
                return(0, "Error: mandatory string not set")
            if len(my_string) > 0: 
                return(1, "mandatory string not empty")
            if len(my_string) == 0:
                return(0, "Error: mandatory string empty")
                
        if template_string.startswith("optional"):
            if my_string == template_string:
                return (1, "Warning: optional parameter not")
            else:
                return(1, "ok: parameter is optional")  
                
        options = get_options(template_string)
        if len(options) > 1:
            if my_string == template_string:
                return(0, "Error: option parameter not set")
            if my_string in options:
                return(1, "ok: Valid option setting")
            else:
                return(0, "Error: Invalid option setting")
        else: 
           
            if not my_string:
               return (0,"Warning: string not set")
            if len(my_string) < 4:
               return (0,"Warning: too short string")
            if my_string == "":
               return (0,"Warning: non mandatory empty string")
            return (0,"Error - uncovered attribute")
    else:
        if key == "report":
            return(0,"See dedicated report summary")
        else:     
            return(-1,"unchecked: specific object type")

def check_in_list(my_string,my_list):
    if my_string in my_list: 
       return 1
    else:
       return 0

def get_workflow_options(project):
    sf_t = utils.generate_project_form(project)
    return sf_t


EXCLUDE_KEYS=['__doc__','i_name','project','report']        
def check_step(sf,sf_t,step):
    ''' Check all components of a workflow step: 
         entity_in, entity_out, agent and activity 
         
         :param sf: form object
         :param step: workflow step
         :returns: dictionary of dictionary, first index: workflow step, 
                    second index: attribute, value: (0 or 1 or -1, "comment")
    '''                
    entity = getattr(sf,step)
    entity_t = getattr(sf_t,step)
    checks={}
    for attr,val in entity.__dict__.items():
        checks[attr]={}
        if attr in config.workflow_steps.WORKFLOW_ENTITIES:
            entity_part = getattr(entity,attr) 
            entity_part_t = getattr(entity_t,attr)
            for key,value in entity_part.__dict__.items():
                if not key in EXCLUDE_KEYS:
                    if hasattr(entity_part_t,key): 
                        value_t = getattr(entity_part_t,key)
                        #print('KEY',key)
                        #print('VALUE',value)
                        checks[attr][key]=check_valid_string(key,value, value_t)
                        #print(checks[attr][key])
                    else:
                        print("Template Warning: no template info for: ",key, "in part ",attr)
    return checks

def check_report(sf,step):
    sf_t = utils.generate_project_form(sf.project)
    report = getattr(getattr(getattr(sf,step),'entity_out'),'report')
    report_t = getattr(getattr(getattr(sf_t,step),'entity_out'),'report')
    checks={}
    for attr,val in report.__dict__.items():
        if not attr in EXCLUDE_KEYS:
            if hasattr(report_t,attr): 
                value_t = getattr(report_t,attr)
                #print('KEY',key)
                #print('VALUE',value)
                checks[attr]=check_valid_string(attr,val, value_t)
                #print(checks[attr][key])
            else:
                print("Template Warning: no template info for: ",attr, "---> ",step)
    return checks
        

def check_step_form(sf,workflow_step):
    sf_t = utils.generate_project_form(sf.project)
    wflow_dict = {}
    wflow_dict[workflow_step] = check_step(sf,sf_t,workflow_step)
    return wflow_dict


def check_generic_form(sf):
    ''' check all components of a workflow form 
    :param sf: workflow form
    :returns: dictionary, index = workflow step, value = check_step result
    '''
    sf_t = utils.generate_project_form(sf.project)
    wflow_dict= {}
    for (step,description) in sf.workflow:     
        wflow_dict[step] = check_step(sf,sf_t,step)
    return wflow_dict 

    
def display_report(check_result):
     display(DictTable(check_result))
     
    

def display_check(check_result,wflow_step):   
        print("=============================================================================")
        print("Workflow step: ",wflow_step)
        for entity in config.workflow_steps.WORKFLOW_ENTITIES:
            print("PROV entity: ", entity)
            display(DictTable(check_result[wflow_step][entity]))
    

def display_checks(sf, check_result):
    for (wflow_step,description) in sf.workflow:
        print("=============================================================================")
        print("Workflow step: ",description)
        for entity in config.workflow_steps.WORKFLOW_ENTITIES:
            print("PROV entity: ", entity)
            display(DictTable(check_result[wflow_step][entity]))




#submission_types = ["initial_submission","new_version","retract"]
#quality_labels = ["no","QC1","QC2-all","QC2-CORDEX","other"]
#terms_of_use = ["non-commercial","commercial"]
#yes_or_no = ["yes","no"]



def list_intersection(list_a,list_b):
    return list(set(list_a) - set(list_b))
    
def check_subset(list_a,list_b):
    return set(list_a) <= set(list_b)

def check_message(result):
    if result == 0 or result == False:
        return "<td style=color:red;>{0}</td>".format("NOT OK")
    else:
        return "<td style=color:green;>{0}</td>".format("OK")


class DictTable(dict):
    # Overridden dict class which takes a dict in the form {'a': 2, 'b': 3},
    # and renders an HTML Table in IPython Notebook.   
    
    def _repr_html_(self):
        
        html = []
        html.append("<p> Summary of check results </p>")
            
        html.append('<table width=100%>')
        html.append("<tr>")
        html.append("<td><b>Value<b></td>")
        html.append("<td><b>Check Result<b></td>")
        html.append("<td><b>Check Comment<b></td>")
        html.append("</tr>")

        
        for key, (val,comm) in sorted(self.items()):
            html.append("<tr>")
            html.append("<td>{0}</td>".format(key))
            html.append(check_message(val))
            html.append("<td>{0}</td>".format(comm))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)
        

#def check_submission(sf):
#    checks = {} 
#    checks["first name"] = check_valid_string(sf.first_name)
#    checks["last name"] = check_valid_string(sf.last_name)
#    checks["email"] = check_email(sf.email) 
#    checks["submission_type"] = check_in_list(sf.submission_type,submission_types)
#    checks["institution"] = check_valid_string(sf.institution)
#    checks["institute_id"] = check_valid_string(sf.institute_id)
#    checks["model_id"] = check_valid_string(sf.model_id)
#    checks["experiment_id"] = check_valid_string(sf.experiment_id)
#    checks["time_period"] = check_valid_string(sf.time_period)
#    checks["grid_mapping_name"] = check_valid_string(sf.grid_mapping_name)
#    checks["grid_as_specified_if_rotated_pole"] = check_in_list(sf.grid_as_specified_if_rotated_pole,yes_or_no)
#    checks["data_qc_status"] = check_in_list(sf.data_qc_status,quality_labels)
#    checks["terms_of_use"] = check_in_list(sf.terms_of_use,terms_of_use)
#    checks["directory_structure"] = check_in_list(sf.directory_structure,["compliant","non-compliant"])
#    checks["exclude_variables_list"] = check_valid_string(sf.exclude_variables_list)
#    checks["uniqueness_of_tracking_id"] = check_in_list(sf.uniqueness_of_tracking_id,yes_or_no)
#    checks["variable_list_day"] = check_subset(variable_list_day,sf.variable_list_day)
#    checks["variable_list_mon"] = check_subset(variable_list_mon, sf.variable_list_mon)
#    checks["variable_list_sem"] = check_subset(variable_list_sem, sf.variable_list_sem)
#    checks["variable_list_fx"] = check_subset(variable_list_fx, sf.variable_list_fx)
#    checks["valid_submission"] = valid_submission(checks) 
#    return checks

def valid_submission(checks):
    summary = True
    for key, val in checks.iteritems():
       summary = (summary and val)
       
    return summary





def check_form(sf,project):
    default_message = {}
    default_message['--- Implementation message: ']='not implemented'
    if project=='ESGF_replication':
        return(True,default_message)
    
    if project=='CMIP6':
        return(True,default_message)
    
    if project=='CORDEX':
        return(True,default_message)
    
    if project=='DKRZ-CDP':
        return(True,default_message)
    else:
        return(False,default_message)
        
        
#---------------------------------
# Project specific checks .. to be generalized ..
def check_file_structure(sf,file_name):
  """ 
  :param arg1: file_name
  :return: status code
  
  Print CORDEX file pattern based on agreed CORDEX DRS structure::
         
      VariableName_Domain_GCMModelName_CMIP5ExperimentName_CMIP5EnsembleMember_RCMModelName
      _RCMVersionID_Frequency[_StartTime - EndTime].nc

  ToDo: replace with generic checking function based on e.g. QA code etc. 
  """
  cordex_template=["VariableName","Domain","GCMModelName","CMIP5ExperimentName","CMIP5EnsembleMember","RCMModelName","RCMVersionID","Frequency","TimeRange"]
  cordex_example = "tas_EUR-44_MPI-M-MPI-ESM-LR_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19710101-19751231.nc"
  print( "Structure: -------" ) 
  print( "DRS key: DRS value")
  print( "------------------"  )
  try:
     file_parts = file_name.split("_") 
     for i,part in enumerate(file_parts):
         print(cordex_template[i],":",part)
     status = True
  except:
     status = False
