"""
Created on Thu Apr 13 18:27:28 2017

@author: stephan
"""
from __future__ import print_function
import os,sys,shutil
from . import utils
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

HOME_DIR = os.environ['HOME']
FORM_REPO = FORM_DIRECTORY
### detecting url of notebook server

if os.getenv('INSTALL_DIRECTORY'):
    INSTALL_DIRECTORY = os.getenv('INSTALL_DIRECTORY')
    vprint("unsing env setting for INSTALL_DIRECTORY:",INSTALL_DIRECTORY)
    
if os.getenv('SUBMISSION_REPO'):
    SUBMISSION_REPO = os.getenv('SUBMISSION_REPO')
    vprint("unsing env setting for SUBMISSION_REPO:",SUBMISSION_REPO)

if os.getenv('NOTEBOOK_DIRECTORY'):
    NOTEBOOK_DIRECTORY = os.getenv('NOTEBOOK_DIRECTORY')
    vprint("unsing env setting for NOTEBOOK_DIRECTORY:",NOTEBOOK_DIRECTORY)

if os.getenv('FORM_REPO'):
    RORM_REPO = os.getenv('FORM_REPO')
    vprint("unsing env setting for FORM_REPO:",FORM_REPO)    



#align_kw = dict(
#    _css = (('.widget-label', 'min-width', '10ex'),),
#    margin = '0px 0px 50px 12px'
#)

# old ,**align_kw  has no effect anymore .. !?
my_layout = Layout(margin='2px 0px 2px 00px')
LAST_NAME = widgets.Text(value="",description="Last name: ",layout=my_layout)
FIRST_NAME = widgets.Text(value="",description="First name: ",layout=my_layout)
EMAIL = widgets.Text(value="", description="Email:",layout=my_layout)
#PROJECT = widgets.Dropdown(description = "Project: ", options=["CORDEX","CMIP6","DKRZ_CDP","ESGF_replication","test","Generic"],**align_kw)
PROJECT = widgets.Dropdown(description = "Project: ", options=["CORDEX","CMIP6","DKRZ_CDP","ESGF_replication","test","Generic"],layout=my_layout)
KEY = widgets.Text(value="", placeholder=" A key to identify your form", description="An identifier: ",layout=my_layout)
# ENTER = widgets.Text(value="", placeholder=" Press \"ENTER\" in this field to initialize your personal form" , description="... " )
ENTER = widgets.Button(value=False, description='Generate form', disabled=False, button_style='', tooltip='click to generate a personal form template', icon='check')
init_widgets=[LAST_NAME,FIRST_NAME,EMAIL,PROJECT,KEY,ENTER]
#---- for selection files
SELECTION = widgets.Button(value=False, description="Save files", disabled=False, button_style='', tooltip='click to save above files')
la = widgets.Layout(height='250px',  width='500px')

#FORMS = widgets.Dropdown(description='Form Name: ',)
FORMS = widgets.Select(description='Form Name: ',)
FORMS_ENTER = widgets.Button(value=False, description='Take selected form', disabled=False, button_style='', tooltip='click to take the selected value above')


TEXT_WIDGETS_DICT = {}
init_widgets=[LAST_NAME,FIRST_NAME,EMAIL,PROJECT,KEY,ENTER]

FORM_NAME = "UNDEFINED"

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

   

def get_selection(val):
    print("Your selection: ", FORMS.value)
    #FORM_NAME = FORMS.value
         
        
def show_selection(): 
    form_info =  form_handler.get_persisted_info(join(HOME_DIR,'fig','keystore'))
    my_options = list(form_info.keys())       
    FORMS.options = my_options
    display(FORMS,FORMS_ENTER)
    FORMS_ENTER.on_click(get_selection)
    return form_info

    
    
def check_and_retrieve(last_name):
    
    info = check_pwd(last_name)
    if info:
        vprint(info)
        vprint("--- copy from:", info['form_path'])
        vprint("--- to: ",join(NOTEBOOK_DIRECTORY,info['project']))
        shutil.copyfile(info['form_path'],join(NOTEBOOK_DIRECTORY,info['project'],info['form_name']+'.ipynb'))
        print("--------------------------------------------------------------------")
        print("   Your submission form was retrieved and is accessible via the following link:")
       
        print(utils.get_formurlpath()+'/'+info['project']+'/'+info['form_name']+'.ipynb')
          ## to do email link to user ....
        print("--------------------------------------------------------------------")
    else:
        print("Error: no corresponding form found")

def fill_form():
    display([LAST_NAME,FIRST_NAME])
    ENTER.on_click(fill)


def fill(val):
    pass
     

def create_form():     
    display(*init_widgets)
    #print "Fill out above fields before entering key below !"
    #check_pwd(LAST_NAME.value)
    #def handle_submit(sender):
    
     #   print FIRST_NAME.valueS
    ENTER.on_click(generate)
     #  FIRST_NAME.on_submit(handle_submit)

def generate(val):
    init_form = {} 
    init_form['first_name'] = FIRST_NAME.value
    init_form['last_name'] = LAST_NAME.value
    init_form['project'] = PROJECT.value
    init_form['email'] = EMAIL.value
    init_form['key'] = KEY.value
    init_form['pwd'] = init_form['project']+'_'+init_form['last_name']+'_'+init_form['key']
    form_handler.generate_submission_form(init_form)
 
    
def save_sel(val):
    selection_dir = join(NOTEBOOK_DIRECTORY,"ESGF_replication","selection")
    for (my_file,val) in TEXT_WIDGETS_DICT.items():
        sel_file_path = join(selection_dir,my_file)
        with open(sel_file_path, 'w') as file_obj:
             print("Selection file: ",my_file," stored")
             sel_text = str(val.value)
             file_obj.write(sel_text)    
    
    
def get_selection_file_contents(file_list):
    selection_dir = join(NOTEBOOK_DIRECTORY,"ESGF_replication","selection")
    print("Retrieving existing selection file information if existing ... ")
    content_list = []
    for my_file in file_list:
        sel_file_path = join(selection_dir,my_file)
        if os.path.isfile(sel_file_path):
            print("Warning: selection file: ",my_file," already exists")
            print("         only modify if it belongs to you !!")
            print("         use other name if it does not belong to you !!!!!")
            with open(sel_file_path, 'r') as file_obj:
                 file_content = file_obj.read()
            content_list.append(file_content)
        else:
            file_content = "# no selection information specified, please fill"
            content_list.append(file_content)        
    return content_list

def get_selection_files(file_list):
    global TEXT_WIDGETS_DICT
    la = widgets.Layout(height='250px',  width='500px')
    content_list = get_selection_file_contents(file_list)
    merge_list = zip(file_list,content_list)
    TEXT_WIDGETS_DICT = {}
    for (my_file,my_content) in merge_list:
        header = "# selection file: "+my_file+"\n \n"
        TEXT_WIDGETS_DICT[my_file] = widgets.Textarea(
                value = header + my_content ,
                place_holder='??',
                disabled = False,
                description = "selection file:",
                layout = la
                )
    return TEXT_WIDGETS_DICT  

def gen_text_widgets(text_w):
    for (key,val) in text_w.items():
        display(val)
    display(SELECTION)
    SELECTION.on_click(save_sel)    
                
