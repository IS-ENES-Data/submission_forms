import sys, os, shutil

#from git import Repo, GitCommandError

join = os.path.join
import_path = os.path.abspath('..')
sys.path.append(import_path)

from dkrz_forms import form_handler, utils

#from dkrz_forms.config.settings import INSTALL_DIRECTORY,  SUBMISSION_REPO, NOTEBOOK_DIRECTORY,FORM_URL_PATH, FORM_REPO
#from dkrz_forms.config.project_config import PROJECT_DICT 
#from dkrz_forms.config.workflow_steps import WORKFLOW_DICT

from dkrz_forms.config.settings import FORM_DIRECTORY
init_form = {}
init_form['first_name'] = "unit_tester"
init_form['last_name'] = "testsuite"
init_form['project'] = "test"
init_form['email'] = "stephan.kindermann@gmail.com"
init_form['key'] = "1" 
init_form['pwd'] = "test1"

FORM_REPO = FORM_DIRECTORY


form_repo = join(FORM_REPO, init_form['project'])
#print test_config.cordex_directory

FORM_JSON = join(form_repo,init_form['project']+'_'+init_form['last_name']+'_'+init_form['key']+'.json')
 

# get workflow steps
#(submission,ingest,checking,publish) = form_handler.get_workflow_steps() 
#print submission.__dict__


#def test_me():
#    assert form_repo == os.path.abspath("....")


def test_init_form():
    global sf
    global init_form
    global form_repo
    
    utils.init_git_repo(form_repo)
    sf = form_handler.init_form(init_form)
    
    assert sf.sub.activity.status == "0:initialized"
    assert os.path.exists(form_repo) == 1
    #assert sf.sub.entity_out.form_repo == FORM_REPO+'/'+init_form['project']
    assert sf.sub.agent.last_name == "testsuite"
    


def test_generate_submission_form():
    ## takes myconfig from .dkrz_forms if existing !! 
    global sf
    global init_form               
    sf = form_handler.generate_submission_form(init_form)
    # .. to do .. make some changes to sf ..
    sf = form_handler.save_form(sf,"test_generate_submission")
    assert sf.sub.activity.status =="1:form_generated"
    #assert sf.form_dir == form_repo
    assert sf.sub.agent.last_name == "testsuite"
    # assert sf.sub.activity. ..  --> to do 
    files = os.listdir(form_repo)
    
    assert sf.sub.entity_out.form_name+".ipynb" in files
    assert sf.sub.entity_out.form_name+".json" in files
    

def test_form_completion():
    ## reads form json file and returns hierachical form object
    global sf
    
    workflow_form = utils.load_workflow_form(FORM_JSON)
    submission = workflow_form.sub
    submission.entity_out.status = "checked"
    submission.activity.status = "3:completed" 
   
    sf = form_handler.save_form(workflow_form, "test: formcompletion()") 
    
    assert sf.sub.entity_out.status == 'checked'
    assert sf.sub.activity.status == '3:completed'
    

def test_form_submission():    
    
    workflow_form = utils.load_workflow_form(FORM_JSON)
    submission = workflow_form.sub
    submission.entity_out.status = "3:submitted"
    submission.activity.handover = "dkrz_staff"
    submission.activity.ticket_id = 22949
    submission.activity.ticket_url = "https://dm-rt.dkrz.de/Ticket/Display.html?id="
    
    sf = form_handler.form_submission(workflow_form)
    
    assert sf.sub.activity.ticket_id == 22949
    
## to do: fill form - check validity - perform submit, check, ingest and publication steps ..
    
def test_form_review():
    workflow_form = utils.load_workflow_form(FORM_JSON)
   
    review = workflow_form.rev
    
    review.activity.responsible_person = "dkrz data manager name"
    review.activity.handover = "dkrz data manager name"
    review.activity.status = "reviewed"
    
    sf = form_handler.save_form(workflow_form, "test: form_review()")
    
    assert sf.rev.activity.status  == "reviewed"
    
    
    
def test_data_ingest():
    workflow_form = utils.load_workflow_form(FORM_JSON)
    
    ingest = workflow_form.ing
    ingest.activity.status = "ingested"
    ingest.activity.responsible_person = "lenzen"
    ingest.activity.comment = " copying data from ... to ... using ... "
    ingest.entity_out.data_target_directory = "/work/kd0956/cmip5/ingest/cmip5/mpi-m/test"
    ingest.entity_out.data_file_pattern = "cmip5"
    
    sf = form_handler.save_form(workflow_form,"test: data_ingest()")
    
    assert sf.ing.activity.status == "ingested"  
    
def test_data_quality_assurance():
    
    
    
    workflow_form = utils.load_workflow_form(FORM_JSON)
    test_report = {
    "QA_conclusion": "PASS",
    "project": "CORDEX",
    "model": "KNMI-RACMO22E",
    "domain": "EUR-11",
    "driving_experiment": [ "ICHEC-EC-EARTH" ],
    "experiment": [ "historical" ],
    "ensemble_member": [ "r12i1p1" ],
    "annotation":
    [
        {
            "scope": [ "mon", "sem" ],
            "variable": [ "sfcWindmax", "sund", "tasmax", "tasmin" ],
            "caption": "Attribute <cell_methods> entails <time>:climatology instead of <time>:time_bnds",
            "comment": "Here, data of variable climatology is equivalent to time_bnds",
            "severity": "note"
        }
    ]
    }
    
    qua = workflow_form.qua
    qua.activity.status = "quality_assured"
    qua.activity.responsible_person = "hdh"
    qua.activity.comment =  "on lizzard "
    qua.activity.handover = "data publisher at DKRZ"
    qua.activity.qa_tool_version = "dkrz_qa_v09"
    qua.entity_out.report = test_report
    
    sf = form_handler.save_form(workflow_form, "test: quality_assurance()")
   
    assert sf.qua.activity.status == "quality_assured" 
    
    
def test_data_publication():
    workflow_form = utils.load_workflow_form(FORM_JSON)
    
    publication = workflow_form.pub    
    
    publication.activity.status = "published"
    publication.activity.responsible_person = "berger"
    publication.activity.timestamp = "2016-05-20 18:34:28.934536"
    publication.entity_out.publication_date = "2016-05-20"
    publication.entity_out.report = "....report on publication...."
    publication.entity_out.search_string = " ... "
    
    sf = form_handler.save_form(workflow_form, "test: publication()")
    
    assert sf.pub.activity.status == "published" 
    
def test_data_archival():
    pass
    
    
    
    

