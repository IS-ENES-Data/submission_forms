# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:27:28 2017

@author: stephan
"""

from ipywidgets import widgets
from IPython.display import display, Javascript, Image
from dkrz_forms import form_handler
from dkrz_forms.config.project_config import FORM_REPO, NOTEBOOK_DIRECTORY, FORM_URL_PATH
import os, shutil

from os.path import join as join

align_kw = dict(
    _css = (('.widget-label', 'min-width', '20ex'),),
    margin = '0px 0px 5px 12px'
)


LAST_NAME = widgets.Text(value="",description="Your last name: ",width=200, **align_kw)
FIRST_NAME = widgets.Text(value="",description="Your first name: ",width=200, **align_kw)
EMAIL = widgets.Text(value="", description="    Your email:",width=200, **align_kw)
PROJECT = widgets.Dropdown(description = "Project selection: ", options=["CORDEX","CMIP6","DKRZ_CDP","ESGF_replication","test","Generic"],**align_kw)
KEY = widgets.Text(value="", description="A key to identifiy your form (confirm with \"ENTER\") ",width=130,**align_kw)
init_widgets=[LAST_NAME,FIRST_NAME,EMAIL,PROJECT,KEY]

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
        print "Unknown status"
        
def check_pwd(last_name):
    form_info = form_handler.get_persisted_info('forms_pwd',join(FORM_REPO,'keystore'))
    
    import getpass
    #my_last_name = getpass.getpass("Enter your last name: ")
    my_pwd = getpass.getpass("Enter your form key: ")
    form_info[my_pwd]['pwd'] = my_pwd
    
    if my_pwd in form_info.keys():
      
        if form_info[my_pwd]['last_name'] == last_name:
            ## 
            
            print "---- Your Name: ", form_info[my_pwd]['first_name'] + " " + form_info[my_pwd]['last_name']
            print "---- Your email: ", form_info[my_pwd]['last_name']
            print "---- Name of this submission form: ", form_info[my_pwd]['form_name']
    
            return form_info[my_pwd]
        else:
            print "Error: incorrect key or incorrcect last name (case sensitive !)" 
            return {}
    else:
         print "Error: incorrect key"
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
       
        print(FORM_URL_PATH+info['project']+'/'+info['form_name']+'.ipynb')
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
    print LAST_NAME.value
    init_form = {} 
    init_form['first_name'] = FIRST_NAME.value
    init_form['last_name'] = LAST_NAME.value
    init_form['project'] = PROJECT.value
    init_form['email'] = EMAIL.value
    init_form['key'] = KEY.value
    form_handler.generate_submission_form(init_form)
    