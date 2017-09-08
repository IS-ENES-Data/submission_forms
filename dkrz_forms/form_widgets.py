# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:27:28 2017

@author: stephan
"""
from __future__ import print_function
import os,sys,shutil
import utils
from os.path import join as join
from os.path import expanduser

from ipywidgets import widgets, Layout, Box
from IPython.display import display, Javascript, Image

from dkrz_forms import form_handler
from notebook import notebookapp

config_file = os.path.join(expanduser("~"),".dkrz_forms")
if os.path.isfile(config_file):
    sys.path.append(config_file)
    CONFIG_FILE = True
else:
    CONFIG_FILE = False
    
if CONFIG_FILE:
   from settings import FORM_DIRECTORY, NOTEBOOK_DIRECTORY
else:    
   from dkrz_forms.config.settings import FORM_DIRECTORY, NOTEBOOK_DIRECTORY
   
VERBOSE = True
def vprint(*txt):
    if VERBOSE:
        print(*txt)
    return  

FORM_REPO = FORM_DIRECTORY
### detecting url of notebook server

if os.getenv('INSTALL_DIRECTORY'):
    INSTALL_DIRECTORY = os.getenv('INSTALL_DIRECTORY')
    vprint("unsing env setting for INSTALL_DIRECTORY:",INSTALL_DIRECTORY)
    
if os.getenv('SUBMISSION_REPO'):
    INSTALL_DIRECTORY = os.getenv('SUBMISSION_REOP')
    vprint("unsing env setting for SUBMISSION_REPO:",SUBMISSION_REPO)

if os.getenv('NOTEBOOK_DIRECTORY'):
    INSTALL_DIRECTORY = os.getenv('NOTEBOOK_DIRECTORY')
    vprint("unsing env setting for NOTEBOOK_DIRECTORY:",NOTEBOOK_DIRECTORY)

if os.getenv('FORM_REPO'):
    INSTALL_DIRECTORY = os.getenv('FORM_REPO')
    vprint("unsing env setting for FORM_REPO:",FORM_REPO)    



align_kw = dict(
    _css = (('.widget-label', 'min-width', '10ex'),),
    margin = '0px 0px 50px 12px'
)

# old ,**align_kw  has no effect anymore .. !?
my_layout = Layout(margin='2px 0px 2px 00px')
LAST_NAME = widgets.Text(value="",description="Last name: ",layout=my_layout)
FIRST_NAME = widgets.Text(value="",description="First name: ",layout=my_layout)
EMAIL = widgets.Text(value="", description="Email:",layout=my_layout)
#PROJECT = widgets.Dropdown(description = "Project: ", options=["CORDEX","CMIP6","DKRZ_CDP","ESGF_replication","test","Generic"],**align_kw)
PROJECT = widgets.Dropdown(description = "Project: ", options=["CORDEX","CMIP6","DKRZ_CDP","ESGF_replication","test","Generic"],layout=my_layout)
KEY = widgets.Text(value="", placeholder=" A short key to remember your form, confirm input with \"ENTER\" ", description="A key: ",layout=my_layout)
ENTER = widgets.Text(value="", placeholder=" Press \"ENTER\" in key field above to initialize your personal form" , description="... " )
init_widgets=[LAST_NAME,FIRST_NAME,EMAIL,PROJECT,KEY,ENTER]

submission_type = widgets.Dropdown(description = "Type of submission: ", options=["initial_version","new_version","retract"])
## maybe move to config part ..

#cordex_sel={}
#cordex_sel['terms_of_use'] = ["unrestricted","non-commercial only"]
#cordex_sel['qc_status'] = ["QC1","QC2","other","unchecked"]

def show_status(status):
    if status == 'form-generation':
        image = Image(filename=join(NOTEBOOK_DIRECTORY,'fig','form-generation.png'))
        display(image)
    elif status == 'form-retrieval':
        image = Image(filename=join(NOTEBOOK_DIRECTORY,'fig','form-retrieval.png'))
        display(image)
    elif status == 'form-submission':
        image = Image(filename=join(NOTEBOOK_DIRECTORY,'fig','form-submission.png'))
        display(image)
    elif status == 'form-dataingest':
        image = Image(filename=join(NOTEBOOK_DIRECTORY,'fig','form-datainges.png'))
        display(image)
    else:
        print("Unknown status")
        
def check_pwd(last_name):
    form_info = form_handler.get_persisted_info('forms_pwd',join(FORM_REPO,'keystore'))
    
    import getpass
    #my_last_name = getpass.getpass("Enter your last name: ")
    my_pwd = getpass.getpass("Enter your form password: ")
    form_info[my_pwd]['pwd'] = my_pwd
    
    if my_pwd in form_info.keys():
      
        if form_info[my_pwd]['last_name'] == last_name:
            ## 
            
            print("---- Your Name: ", form_info[my_pwd]['first_name'] + " " + form_info[my_pwd]['last_name'])
            print("---- Your email: ", form_info[my_pwd]['last_name'])
            print("---- Name of this submission form: ", form_info[my_pwd]['form_name'])
    
            return form_info[my_pwd]
        else:
            print("Error: incorrect key or incorrcect last name (case sensitive !)" )
            return {}
    else:
         print("Error: incorrect key")
         return False

def check_and_retrieve(last_name):
    
    info = check_pwd(last_name)
    if info:
        print(info)
        print("--- copy from:", info['form_path'])
        print("--- to: ",join(NOTEBOOK_DIRECTORY,info['project']))
        shutil.copyfile(info['form_path'],join(NOTEBOOK_DIRECTORY,info['project'],info['form_name']+'.ipynb'))
        print("--------------------------------------------------------------------")
        print("   Your submission form was retrieved and is accessible via the following link:")
       
        print(utils.get_formurlpath()+'/'+info['project']+'/'+info['form_name']+'.ipynb')
          ## to do email link to user ....
        print("--------------------------------------------------------------------")


        

def create_form():     
    display(*init_widgets)
    #print "Fill out above fields before entering key below !"
    #check_pwd(LAST_NAME.value)
    #def handle_submit(sender):
    
     #   print FIRST_NAME.valueS
    KEY.on_submit(generate)
     #  FIRST_NAME.on_submit(handle_submit)

def generate(val):
    init_form = {} 
    print("Value:  ", val)
    init_form['first_name'] = FIRST_NAME.value
    init_form['last_name'] = LAST_NAME.value
    init_form['project'] = PROJECT.value
    init_form['email'] = EMAIL.value
    init_form['key'] = KEY.value
    form_handler.generate_submission_form(init_form)
    
