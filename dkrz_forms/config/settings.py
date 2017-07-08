# -*- coding: utf-8 -*-
# 
# Created on Thu May 18 10:55:26 2017
#
# @author: stephan
"""

Generic settings
=================================================

*Adapt to your environment*:

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
    a directory where all form notebooks are stored (normally in git repos)
    
SUBMISSION_REPO:
    a directory (under git control) where all finalized data form notebooks 
    and form information ist stored  

"""

# --------------------------------------------------------------------------
# directory where submission_forms package is installed
# 
# INSTALL_DIRECTORY = "pip" 
INSTALL_DIRECTORY = "/home/stephan/Repos/"
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Directory where web accessible forms are served
# - a jupyter notebook server accessible directory whre forms are served
NOTEBOOK_DIRECTORY = '/home/stephan/Repos/submission_forms/test/forms'
#---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# directory containing the git repositories where forms are locally stored
# - all the forms currently not finalized and submitted are stored here
# - normally git versioned 
# - should contain directories corresponding to every project type supported
#   e.g. CMIP6, DKRZ_CDP, test
#   these directories should be git versioned
# - access keys for the forms are stored in a keystore file 

FORM_DIRECTORY = "/home/stephan/tmp/Repos/"
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# finalised form storage directory 
# - for end user side installation this containes the finalised forms to be
#   submitted to the data center
# - for data manager side installation the contained repos are synchronized 
#   with the gitlab hosted master ... 
SUBMISSION_REPO = "/home/stephan/tmp/Repos/submission_repo"
# ---------------------------------------------------------------------------


