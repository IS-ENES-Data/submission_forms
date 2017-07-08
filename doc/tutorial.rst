
Tutorial 
=============

In the following short introductions are given for the different application
scenarios:

* Using a data center side deployment of the form interfaces 
* Using the forms client side (data provider side)
* Data manager side use of provided tools supporting the data ingest workflow 

Using the DKRZ online form 
-----------------------------

.. to be finalized before Oct. 2017
Follow the instructions published at https://redmine.dkrz.de/dkrz_cdp and 
log into the forms portal at https://forms.dkrz.de:8080/create.ipynb

To retrieve and complete forms you started to fill in the past, go to 
https://forms.dkrz.de:8080/retrieve.ipynb

Using these entry points your can create new personal interactive forms.
These forms collect project specific information needed by the data center to manage the data ingest workflow.

After finalising the forms, they are checked and stored. You are notified via mail about your data ingest request. 
Also the data managers at the data center are notified.
They will let you know about open issues to resolve as well as the status of the data ingest process.


Client side installation and usage
------------------------------------

Installing from github
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Download the sources from https://github.com/IS-ENES-Data/submission_forms.git::

      git clone https://github.com/IS-ENES-Data/submission_forms.git
  
  The directory you downloaded the sources to will be named "INSTALLATION_DIR" in the following 

* Configure your python path as well as the directories used for form storage::

      export PYTHONPATH="INSTALLATION_DIR":$PYTHONPATH
      
  follow the instructions provided in "INSTALLATION_DIR"/config/dkrz_forms/settings.py 
  as part of this you have to provide a directory where you want your ipython notebook based forms, 
  its called "NOTEBOOK_DIRECTORY"
  
  
  copy the initial notebook forms into your "NOTEBOOK_DIRECTORY"::
  
       cp "INSTALLATION_DIR"/submission_forms/dkrz_forms/Templates/Create_Submission_Form.ipynb "NOTEBOOK_DIRECTORY"
       cp "INSTALLATION_DIR"/submission_forms/dkrz_forms/Templates/Retrieve_Form.ipynb "NOTEBOOK_DIRECTORY"
       
* start your notebook server and access the forms in "NOTEBOOK_DIRECTORY"       

* have a look at the tutorial notebooks at https://github.com/IS-ENES-Data/submission_forms/tutorials 
      

Installing via pip / setup tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The package is not yet available in the global pip packet index.
It will be published there after final adaptations based on first application
experiences in real production scenarios.

For the time being pip/setuptools based installation is not recommended but possible by:
* downloading the source from github (see previous section)
* cd /"your_download_dir"/submission_forms
* python setup.py install



Data manager side usage
-------------------------

* Generic usage pattern

    * Sync the global submission from central gitlab repo
    * load and modify the json files corresponding to a specific data ingest activity.
    * store the results in the central gitlab repo

    see the tutorial notebooks for the recommended steps according to the individual data ingest workflow steps corresponding to
    
    * data form checking
    * data transfer and data center side storage
    * data quality assurance
    * data publication
    * data archival

* Specific examples

.. to be filled 



