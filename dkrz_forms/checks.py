import re
# from collections import OrderedDict

def check_email(email):
    if re.match(""r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email) != None:
       return 1
    else: 
       return 0

def check_valid_string(my_string):
    if not my_string:
       return 0 
    if my_string == "...":
       return 0
    return 1

def check_in_list(my_string,list):
    if my_string in submission_types: 
       return 1
    else:
       return 0


submission_types = ["initial_submission","new_version","retract"]
quality_labels = ["no","QC1","QC2-all","QC2-CORDEX","other"]
terms_of_use = ["non-commercial","commercial"]
yes_or_no = ["yes","no"]

variable_list_day = [
"clh","clivi","cll","clm","clt","clwvi",
"evspsbl","evspsblpot",
"hfls","hfss","hurs","huss","hus850",
"mrfso","mrro","mrros","mrso",
"pr","prc","prhmax","prsn","prw","ps","psl",
"rlds","rlus","rlut","rsds","rsdt","rsus","rsut",
"sfcWind","sfcWindmax","sic","snc","snd","snm","snw","sund",
"tas","tasmax","tasmin","tauu","tauv","ta200","ta500","ta850","ts",
"uas","ua200","ua500","ua850",
"vas","va200","va500","va850","wsgsmax",
"zg200","zg500","zmla"
]

variable_list_mon = [
"clt",
"evspsbl",
"hfls","hfss","hurs","huss","hus850",
"mrfso","mrro","mrros","mrso",
"pr","psl",
"rlds","rlus","rlut","rsds","rsdt","rsus","rsut",
"sfcWind","sfcWindmax","sic","snc","snd","snm","snw","sund",
"tas","tasmax","tasmin","ta200",
"ta500","ta850",
"uas","ua200","ua500","ua850",
"vas","va200","va500","va850",
"zg200","zg500"
]
variable_list_sem = [
"clt",
"evspsbl",
"hfls","hfss","hurs","huss","hus850",
"mrfso","mrro","mrros","mrso",
"pr","psl",
"rlds","rlus","rlut","rsds","rsdt","rsus","rsut",
"sfcWind","sfcWindmax","sic","snc","snd","snm","snw","sund",
"tas","tasmax","tasmin","ta200","ta500","ta850",
"uas","ua200","ua500","ua850",
"vas","va200","va500","va850",
"zg200","zg500"  
]

variable_list_fx = [
"areacella",
"mrsofc",
"orog",
"rootd",
"sftgif","sftlf"   
]


def list_intersection(list_a,list_b):
    return list(set(list_a) - set(list_b))
    
def check_subset(list_a,list_b):
    return set(list_a) <= set(list_b)

def check_message(value):
    if value == 0 or value == False:
        return "<td style=color:red;>{0}</td>".format("ERROR")
    else:
        return "<td style=color:green;>{0}</td>".format("OK")

class DictTable(dict):
    # Overridden dict class which takes a dict in the form {'a': 2, 'b': 3},
    # and renders an HTML Table in IPython Notebook.
    def _repr_html_(self):
        html = []
        if not self['valid_submission']:
            html.append("<p style=color:red;> Attention: your submission is incomplete and not yet ready for submission </p>")
            html.append("<p> Please see the following check summary: </p>")
        else:
            html.append("<p> Your submission is ready for submission </p>")
            
        html.append('<table width=100%>')
        html.append("<tr>")
        html.append("<td><b>Value<b></td>")
        html.append("<td><b>Check<b>Result</td>")
        html.append("</tr>")
        
        for key, value in sorted(self.items()):
            html.append("<tr>")
            html.append("<td>{0}</td>".format(key))
            html.append(check_message(value))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)

def check_result(val):
    if check_result == 1:
       return "ok"
    else:
       return "Error"

def check_submission(sf):
    checks = {} 
    checks["first name"] = check_valid_string(sf.first_name)
    checks["last name"] = check_valid_string(sf.last_name)
    checks["email"] = check_email(sf.email) 
    checks["submission_type"] = check_in_list(sf.submission_type,submission_types)
    checks["institution"] = check_valid_string(sf.institution)
    checks["institute_id"] = check_valid_string(sf.institute_id)
    checks["model_id"] = check_valid_string(sf.model_id)
    checks["experiment_id"] = check_valid_string(sf.experiment_id)
    checks["time_period"] = check_valid_string(sf.time_period)
    checks["grid_mapping_name"] = check_valid_string(sf.grid_mapping_name)
    checks["grid_as_specified_if_rotated_pole"] = check_in_list(sf.grid_as_specified_if_rotated_pole,yes_or_no)
    checks["data_qc_status"] = check_in_list(sf.data_qc_status,quality_labels)
    checks["terms_of_use"] = check_in_list(sf.terms_of_use,terms_of_use)
    checks["directory_structure"] = check_in_list(sf.directory_structure,["compliant","non-compliant"])
    checks["exclude_variables_list"] = check_valid_string(sf.exclude_variables_list)
    checks["uniqueness_of_tracking_id"] = check_in_list(sf.uniqueness_of_tracking_id,yes_or_no)
    checks["variable_list_day"] = check_subset(variable_list_day,sf.variable_list_day)
    checks["variable_list_mon"] = check_subset(variable_list_mon, sf.variable_list_mon)
    checks["variable_list_sem"] = check_subset(variable_list_sem, sf.variable_list_sem)
    checks["variable_list_fx"] = check_subset(variable_list_fx, sf.variable_list_fx)
    checks["valid_submission"] = valid_submission(checks) 
    return checks

def valid_submission(checks):
    summary = True
    for key, val in checks.iteritems():
       summary = (summary and val)
       
    return summary


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
