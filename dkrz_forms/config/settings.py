# -*- coding: utf-8 -*-
# 
# Created on Thu May 18 10:55:26 2017
#
# @author: stephan
"""

Generic settings
=================================================

Warning: leave the default settings 
   - just adapt in case of server based deployments
   - (e.g. for jupyterhub deployments)
   
Settings for the installation home and the three storage locations you need:

    either change settings in this file, or put a copy of this file in your working directory nder "settings.py"
        (where you start your notebook server and start ipython sessions)   

INSTALL_DIRECTORY: 
    if package was installed from source (github) specify the installation directory 
       ( INSTALL_DIRECTORY = "path_where_i_cloned_the_git_repo" )
         INSTALL_DIRECTORY = "" or "pip" when installed via pip )
    
NOTEBOOK_DIRECTORY: 
    a directory where the notebook serves all the form notebooks
    
FORM_DIRECTORY:
    a directory where all form notebooks are locally stored (in repos)
    
SUBMISSION_REPO:
    a directory (under git control) where all finalized data form notebooks 
    and form information ist stored  

"""
import os
# --------------------------------------------------------------------------
# directory where submission_forms package is installed
# 
INSTALL_DIRECTORY = "pip" 
#INSTALL_DIRECTORY = "/home/stephan/Repos/"
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Directory where web accessible forms are served
# - a jupyter notebook server accessible directory where forms are served
# not needed for jupyterhub deployment (home directory in this case)
NOTEBOOK_DIRECTORY = os.path.join(os.environ['HOME'],'Forms')
#---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# directory containing the git repositories where forms are locally stored 
# for testing and local deployment scenarios 
# for jupyterhub based scenario just used for testing ..
# - all the forms currently not finalized and submitted are stored here
# - normally git versioned 
# - should contain directories corresponding to every project type supported
#   e.g. CMIP6, DKRZ_CDP, test
#   these directories should be git versioned
# - access keys for the forms are stored in a keystore file 


FORM_DIRECTORY = os.path.join(NOTEBOOK_DIRECTORY,"form_directory")
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# finalised form storage directory 
# - for end user side installation this containes the finalised forms to be
#   submitted to the data center
# - for data manager side installation the contained repos are synchronized 
#   with the gitlab hosted master ... 
SUBMISSION_REPO = os.path.join(NOTEBOOK_DIRECTORY,"submission_repo")
# ---------------------------------------------------------------------------
# Initialization directory -- moved to home directory of user 
# in jupyter notebook or juypterlab environment

#INIT_DIR = "/opt/jupyter/Forms"

BASE_URL = "http://localhost:8888"

SERVER = "notebook"   # or "jupyterhub"
