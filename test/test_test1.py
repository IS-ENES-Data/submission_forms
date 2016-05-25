
import sys, os, shutil

from git import Repo, GitCommandError

"""
to do: import publish etc dict as objects
       assign value based on objects (with then predefined attributes)


"""
join = os.path.join
import_path = os.path.abspath('..')
sys.path.append(import_path)

from dkrz_forms import form_handler
from dkrz_forms.config import test_config
from dkrz_forms.config import workflow_steps

#print test_config.cordex_directory
project_dir = test_config.cordex_directory

# get workflow steps
#(submission,ingest,checking,publish) = form_handler.get_workflow_steps() 

#print submission.__dict__


def init_git_repo(target_dir):
    if os.path.exists(target_dir):
       shutil.rmtree(target_dir)
    repo = Repo.init(target_dir)
    return repo


    

## generic settings for tests
my_first_name = "stasi"  # example: my_first_name = "Alf"
my_last_name = "ki"   # example: my_last_name = "Mitty"
my_email = "snkinder@freenet.de"       # example: email = "alf.mitty@gmail.com"
my_project = "CORDEX"  # available alternatives: "Test", "CORDEX","CMIP6","Other"
my_keyword = "sk1"     # please remember your personal keyword to identify your submission

form_info_json_file = project_dir + "/" + my_last_name+"_"+my_keyword+".json"



def test_me():
    assert project_dir == '/home/stephan/tmp/CORDEX'


def test_formgeneration():
    ## takes myconfig from .dkrz_forms if existing !! 
   
    init_git_repo(project_dir)                 
    form_handler.generate_submission_form(my_first_name,my_last_name,my_email,my_project,my_keyword)
    assert os.path.exists(project_dir) == 1
    files = os.listdir(project_dir)
    print files
    assert my_last_name+"_"+my_keyword+".ipynb" in files 
    assert my_last_name+"_"+my_keyword+".json" in files


def test_formcompletion():
    ## reads form json file and returns hierachical form object
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    submission = workflow_form.sub
    submission.status = "checked"
    submission.check_status = "consistency_checked"
   
    form_handler.save_form(workflow_form, "test: formcompletion()") 
    #test_dict['sub']['status'] = "checked"
    #test_dict['sub']['check_status'] = "consistency_checked"
    #test_form = form_handler.dict_to_form(test_dict)
    
    #form_handler.form_save(test_form)
   
    #test_dict2 = form_handler.jsonfile_to_dict(form_info_json_file)
    
    assert workflow_form.sub.status == 'checked'
    assert workflow_form.sub.check_status =="consistency_checked"
    
    #test_hform = form_handler.dict_to_hform(test_dict)
    #print test_hform.sub

def test_formsubmission():    
    
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    submission = workflow_form.sub
    submission.status = "submitted"
    submission.responsible_person = "dkrz_staff"
    submission.ticket_id = 22949
    submission.ticket_url = "https://dm-rt.dkrz.de/Ticket/Display.html?id="
    
    form_handler.save_form(workflow_form, "test: formsubmission()")
    
    assert workflow_form.sub.ticket_id == 22949
    
## to do: fill form - check validity - perform submit, check, ingest and publication steps ..
    
def test_formcheck_start():
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    submission = workflow_form.sub
    
    submission.status = "form_checking"
    submission.responsible_person = "lenzen"
    
    form_handler.save_form(workflow_form, "test: formcheck_start()")
    
    assert submission.status == "form_checking"
    
    
def test_formcheck_end():
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    submission = workflow_form.sub
    
    submission.status = "finalised"
    submission.comment = "terms of use clarified"
    
    form_handler.save_form(workflow_form, "test: formcheck_end()")
    
    assert submission.status == "finalised"   
    
def test_dataingest_start():
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    ingest = workflow_form.ing
    ingest.status = "ingesting"
    ingest.responsible_person = "lenzen"
    ingest.comment = " copying data from ... to ... using ... "
    ingest.target_directory = "/work/kd0956/cmip5/ingest/cmip5/mpi-m/test"
    
    form_handler.save_form(workflow_form,"test: dataingest_start()")
    
    assert ingest.status == "ingesting"
    
    
def test_dataingest_end():    
    
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    ingest = workflow_form.ing
    ingest.status = "ingested"
    ingest.comment = ingest.comment + " time: about 2 hours, volume: about .. GB "
    ingest.drs_file_pattern = "project:cmip5 | experiment:test| variables: tua,uav"
    
    form_handler.save_form(workflow_form,"test:dataingest_end()")
    
    assert ingest.status == "ingested"  
    
def test_datacheck_start():
    
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    
    qua = workflow_form.qua
    qua.status = "checking"
    qua.responsible_person = "hdh"
    qua.comment =  "on lizzard "
    qua.qa_tool_version = "dkrz_qa_v09"
    
    form_handler.save_form(workflow_form, "test: datacheck_start()")
   
    assert qua.status == "checking" 
    
def test_datacheck_end():
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    qua = workflow_form.qua
    qua.status = "checked"
    qua.target_directory = "/work/KD0956/qa_results/cmip5/mpi-m/test"
    
    form_handler.save_form(workflow_form, "test: datacheck_end()")
    
    assert qua.status == "checked" 
    
def test_publish_start():
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    publication = workflow_form.pub    
    
    publication.status = "publishing"
    publication.responsible_person = "berger"
    publication.timestamp = "2016-05-20 18:34:28.934536"
    
    form_handler.save_form(workflow_form, "test: publish_start()")
    
    assert publication.status == "publishing" 

def test_publish_end():
    workflow_form = form_handler.load_workflow_form(form_info_json_file)
    publication = workflow_form.pub  
    
    publication.status = "published"
    publication.publish_date = "2016-05-20 19"
    publication.search_string = "&model=cmip5&experiment=test"
    publication.map_file = "host://path_to_mapfile" 
    
    form_handler.save_form(workflow_form, "test: publish_end()")
    
    assert publication.status == "published"       
    
    
    
    
    
    

