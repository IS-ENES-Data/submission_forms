# -*- coding: utf-8 -*-
"""

Generic settings
=================================================

*Adapt to your environment*:

Settings for the installation home and the three storage locations you need:

* INSTALL_DIRECTORY: 
    if package was installed from source (github) specifyy the installation directory 
    
* NOTEBOOK_DIRECTORY: 
    a directory where the notebook serves all the form notebooks
    
* FORM_DIRECTORY:
    a directory where all form notebooks are stored
    
* SUBMISSION_REPO:
    a directory (under git versioning control) where all finalized data form notebooks 
    and form information ist stored  
# 
# 
Created on Thu May 18 10:55:26 2017

@author: stephan
"""

# directory where submission_forms package is installed
# 
# use INSTLL_DIRECTORY = "pip" in case FormFabric was installed via pip
INSTALL_DIRECTORY = "/home/stephan/Repos/"

# Directory where web accessible forms are served
NOTEBOOK_DIRECTORY = '/home/stephan/Repos/submission_forms/test/forms'

# Url where notebooks are served ..
# FORM_URL_PATH = 'http://localhost:8888/notebooks/Repos/ENES-EUDAT/submission_forms/test/forms/'


# temporary form storage directory
# - all the forms currently not finalized and submitted are stored here
# - normally git versioned 
# - access keys for the forms are stored in keystore_path  which is set to join(FORM_REPO,keystore)
FORM_DIRECTORY = "/home/stephan/tmp/Repos/"
#DIR_PREFIX = "/home/stephan/tmp/Repos/"    # for json db storage
#FORM_REPO = DIR_PREFIX+'form_repo'


# final form storage directory (normally git repo synchr. with gitlab)
SUBMISSION_REPO = "/home/stephan/tmp/Repos/submission_repo"



