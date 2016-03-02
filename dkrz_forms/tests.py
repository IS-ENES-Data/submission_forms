import re
# from collections import OrderedDict

def test_email(email):
    if re.match(""r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email) != None:
       return 1
    else: 
       return 0

def test_valid_string(my_string):
    if not my_string:
       return 0 
    if my_string == "...":
       return 0
    return 1

def test_in_list(my_string,list):
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
    
def test_subset(list_a,list_b):
    return set(list_a) <= set(list_b)


class DictTable(dict):
    # Overridden dict class which takes a dict in the form {'a': 2, 'b': 3},
    # and renders an HTML Table in IPython Notebook.
    def _repr_html_(self):
        html = ["<table width=100%>"]
        html.append("<tr>")
        html.append("<td><b>Value<b></td>")
        html.append("<td><b>Check<b>Result</td>")
        html.append("</tr>")
        for key, value in sorted(self.items()):
            html.append("<tr>")
            html.append("<td>{0}</td>".format(key))
            html.append("<td>{0}</td>".format(value))
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
    checks["first name"] = test_valid_string(sf.first_name)
    checks["last name"] = test_valid_string(sf.last_name)
    checks["email"] = test_email(sf.email) 
    checks["submission_type"] = test_in_list(sf.submission_type,submission_types)
    checks["institution"] = test_valid_string(sf.institution)
    checks["institute_id"] = test_valid_string(sf.institute_id)
    checks["model_id"] = test_valid_string(sf.model_id)
    checks["experiment_id"] = test_valid_string(sf.experiment_id)
    checks["time_period"] = test_valid_string(sf.time_period)
    checks["grid_mapping_name"] = test_valid_string(sf.grid_mapping_name)
    checks["grid_as_specified_if_rotated_pole"] = test_in_list(sf.grid_as_specified_if_rotated_pole,yes_or_no)
    checks["data_qc_status"] = test_in_list(sf.data_qc_status,quality_labels)
    checks["terms_of_use"] = test_in_list(sf.terms_of_use,terms_of_use)
    checks["directory_structure"] = test_in_list(sf.directory_structure,["compliant","non-compliant"])
    checks["exclude_variables_list"] = test_valid_string(sf.exclude_variables_list)
    checks["uniqueness_of_tracking_id"] = test_in_list(sf.uniqueness_of_tracking_id,yes_or_no)
    checks["variable_list_day"] = test_subset(variable_list_day,sf.variable_list_day)
    checks["variable_list_mon"] = test_subset(variable_list_mon, sf.variable_list_mon)
    checks["variable_list_sem"] = test_subset(variable_list_sem, sf.variable_list_sem)
    checks["variable_list_fx"] = test_subset(variable_list_fx, sf.variable_list_fx)   
    return checks

def valid_submission(checks):
    for key, val in checks:
       if not val: 
          return 0
       return 1




