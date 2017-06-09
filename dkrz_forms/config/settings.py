# -*- coding: utf-8 -*-
"""

Generic settings
=================================================

*Adapt to your environment*:

Settings for:

* form storage locations (directories)
* form web access prefix
* installation location

source is self-exploining - follow instructions there to adapt to your environment

# 
# 
Created on Thu May 18 10:55:26 2017

@author: stephan
"""

# directory where submission_forms package is installed
# 
# use INSTLL_DIRECTORY = "pip" in case FormFabric was installed via pip
INSTALL_DIRECTORY = "/home/stephan/Repos/ENES-EUDAT/"

# Directory where web accessible forms are served
NOTEBOOK_DIRECTORY = '/home/stephan/Repos/ENES-EUDAT/submission_forms/test/forms'

# Url where notebooks are served ..
FORM_URL_PATH = 'http://localhost:8888/notebooks/Repos/ENES-EUDAT/submission_forms/test/forms/'


# temporary form storage directory
# - all the forms currently not finalized and submitted are stored here
# - normally git versioned 
# - access keys for the forms are stored in keystore_path  which is set to join(FORM_REPO,keystore)
FORM_REPO = "/home/stephan/tmp/Repos/form_repo"


# final form storage directory (normally git repo synchr. with gitlab)
SUBMISSION_REPO = "/home/stephan/tmp/Repos/submission_repo"


# Root directory where the form information is persisted
# - used for json database backend
DIR_PREFIX = "/home/stephan/tmp/Repos/"    # for json db storage
