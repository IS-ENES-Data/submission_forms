# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:55:26 2017

@author: stephan
"""

# directory where submission_forms package is installed
# leave empty if pip installed
# install_directory = "/opt/formhandler/"
INSTALL_DIRECTORY = "/home/stephan/Repos/ENES-EUDAT/"

# Directory where web accessible forms are served
NOTEBOOK_DIRECTORY = '/home/stephan/Repos/ENES-EUDAT/submission_forms/test/forms'

# Url where notebooks are served ..
FORM_URL_PATH = 'http://localhost:8888/notebooks/Repos/ENES-EUDAT/submission_forms/test/forms/'
# Directory where the project git repos live
# dir_prefix = "/opt/formhandler/Repos/"
DIR_PREFIX = "/home/stephan/tmp/Repos/"    # for json db storage

# keystore_path is set to join(FORM_REPO,keystore) 

FORM_REPO = "/home/stephan/tmp/Repos/form_repo"

# final submissions repo (gitlab synchronized)
SUBMISSION_REPO = "/home/stephan/tmp/Repos/submission_repo"