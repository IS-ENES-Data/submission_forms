import sys, os, shutil
from datetime import datetime
#from git import Repo, GitCommandError

join = os.path.join
import_path = os.path.abspath('..')
sys.path.append(import_path)

from dkrz_forms import form_handler, utils

#from dkrz_forms.config.settings import INSTALL_DIRECTORY,  SUBMISSION_REPO, NOTEBOOK_DIRECTORY,FORM_URL_PATH, FORM_DIRECTORY
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

form_repo = join(FORM_DIRECTORY, init_form['project'])
#print test_config.cordex_directory

FORM_JSON = join(form_repo,init_form['project']+'_'+init_form['last_name']+'_'+init_form['key']+'.json')
 

# get workflow steps
#(submission,ingest,checking,publish) = form_handler.get_workflow_steps() 
#print submission.__dict__


#def test_me():
#    assert form_repo == os.path.abspath("....")
# activity  'status':'0:initialized, 1:generated,2:checked, 2:incomplete,3:submitted,4:re-opened,5:re-submitted',
# entity out 'status': '0:open,1:stored,2:submitted,2:accepted',
# entity_out          'check_status' : "0:open,1:warning,2:error,3:ok",

def now():
    return str(datetime.now())

def test_init_form():
    global sf
    global init_form
    global form_repo
    
    utils.init_git_repo(form_repo)
    sf = form_handler.init_form(init_form)
    
    assert sf.sub.activity.status == "0:open"
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
    assert sf.sub.activity.status =="1:in-progress"
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
    
    submission.activity.start_time = now()
    submission.activity.status = "2:action-required" 
    submission.activity.error_status = "1:ok"
   
    sf = form_handler.save_form(workflow_form, "test: formcompletion()") 
    
    assert sf.sub.entity_out.status == '1:stored'
    assert sf.sub.activity.status == '2:action-required'
    

def test_form_submission():    
    global sf
    workflow_form = utils.load_workflow_form(FORM_JSON)
    submission = workflow_form.sub
    
    #to do: fix submission test
    submission.entity_out.submission_json  = "tst.json"
    submission.entity_out.submission_form = "tst.ipynb"
    submission.entity_out.submission_repo = "."

    submission.activity.ticket_id = 22949
    submission.activity.ticket_url = "https://dm-rt.dkrz.de/Ticket/Display.html?id="
    submission.entity_out.check_status = "3:ok"
    submission.entity_out.status = "1:stored"
    submission.entity_out.checks_done = "consistency with templates"
    submission.activity.method = "form_based"
    
    workflow_form.rev.entity_in = submission.entity_out
    sf = form_handler.save_form(workflow_form, "test: form_submission")
    
    assert sf.sub.activity.ticket_id == 22949
    
## to do: fill form - check validity - perform submit, check, ingest and publication steps ..
    
def test_form_review():
    global sf
    workflow_form = utils.load_workflow_form(FORM_JSON)
   
    review = workflow_form.rev
    review.activity.ticket_url="https://dm-rt.dkrz.de/Ticket/Display.html?"
    
    review.agent.responsible_person = "dkrz data manager name"
    
    review.activity.status = "1:in-progress"
    review.activity.status = "4:closed"
    review.activity.error_status = "1:ok"
    review.activity.start_time = now()
    review.activity.ticket_id = "1:testticket"
    review.entity_out.check_status = "3:ok"
    review.entity_out.status = "1:stored"
    review.entity_out.date = now()
    
    workflow_form.ing.entity_in = review.entity_out 
    sf = form_handler.save_form(workflow_form, "test: form_review()")
    
    assert sf.rev.activity.status  == "4:closed"
    
    
    
def test_data_ingest():
    global sf
    workflow_form = utils.load_workflow_form(FORM_JSON)
    
    ingest = workflow_form.ing
    ingest.activity.status = "1:in-progress"
    ingest.agent.responsible_person = "lenzen"
    ingest.activity.comment = " copying data from ... to ... using ... "
    ingest.entity_out.report.data_target_directory = "/work/kd0956/cmip5/ingest/cmip5/mpi-m/test"
    ingest.entity_out.report.data_file_pattern = "cmip5"
    ingest.activity.status = "2:action-required"
    ingest.activity.status = "4:closed"
    ingest.activity.error_status = "1:ok"
    ingest.activity.ticket_id = "1:testticket"
    ingest.entity_out.check_status = "3:ok"
    ingest.entity_out.status = "1:stored"
    ingest.activity.start_time = now()
    ingest.entity_out.date = now()
    ingest.entity_out.status = "1:stored"
    
    workflow_form.qua.entity_in = ingest.entity_out
    sf = form_handler.save_form(workflow_form,"test: data_ingest()")
    
    assert sf.ing.activity.status == "4:closed"  
    
def test_data_quality_assurance():
    
    global sf
    
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
    qua.activity.status = "1:in-progress"
    qua.agent.responsible_person = "hdh"
    qua.activity.comment =  "on lizzard "

    qua.activity.qua_tool_version = "dkrz_qa_v09"
    qua.activity.start_time = now()
    qua.entity_out.report = test_report
    qua.activity.status = "2:action-required"
    qua.activity.status = "4:closed"
    qua.activity.error_status = "1:ok"
    qua.activity.ticket_id = "1:testticket"
    qua.entity_out.check_status = "3:ok"
    qua.entity_out.status = "1:stored"
    qua.entity_out.date = now()

    
    workflow_form.pub.entity_in = qua.entity_out
    sf = form_handler.save_form(workflow_form, "test: quality_assurance()")
   
    assert sf.qua.activity.status == "4:closed" 
    
    
def test_data_publication():
    global sf
    workflow_form = utils.load_workflow_form(FORM_JSON)
    
    publication = workflow_form.pub    
    
    publication.activity.status = "1_in-progress"
    publication.activity.start_time = now()
    publication.agent.responsible_person = "berger"
    publication.agent.trigger="other"
    publication.activity.timestamp = "2016-05-20 18:34:28.934536"
    publication.entity_out.date = "2016-05-20"
    publication.entity_out.report = "....report on publication...."
    publication.entity_out.search_string = " ... "
    publication.activity.status = "4:closed"
    publication.activity.error_status = "1:ok"
    publication.entity_out.check_status = "3:ok"
    publication.entity_out.status = "1:stored"
    publication.activity.ticket_id = "1:testticket"
    
   # workflow_form.lta ...
    sf = form_handler.save_form(workflow_form, "test: publication()")
    
    assert sf.pub.activity.status == "4:closed" 
    
def test_data_archival():
    pass
    
    
    
    

