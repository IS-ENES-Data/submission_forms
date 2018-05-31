# submission_forms: components and workflow support for data ingest activities

a data submission workflow normally is based on the following steps:
* information collection to manage the specific data ingest request
* data ingest
* data quality assurance
* data publication (making data accessible in file system or via portals)
* data archival 

The submission_forms package provides:
* interactive ipython notebooks for data submission related information collection 
* a set of utilities to store and manage submission information (json based)
* a set of utilities for data managers to manage submission related information based on json as well as an object representation of json information. 
* a tranformation of this information to a W3C Prov representation (xml, json as well as graph)


## Installation

* Dependencies:
   * a python 3 installation with ipython and jupyter notebook support
   * a conda based python (3.x) installation (https://www.continuum.io/downloads) is recommended 
   * dependencies: 
        * ipython, notebook, matplotlib (optional)
        * other dependencies are installed automatically (like prov, gitpython, ..)
   * to satisfy dependencies e.g. do
        * conda install ipython, notebook, gitpython, matplotlib
      
* Installation:
  A future version will provide direct installation via pip, for the time being pip install the version on github:    
  * git clone https://github.com/IS-ENES-Data/submission_forms.git
  * cd ..your_installation_path/submission_forms.git 
  * pip install . 
     * this installs the dkrz_forms package in your current python environment
     * it is recommended to use a separate python environment for this


## Usage and Documentation

1. Run in your home directory **init_forms**
   * This will generate a prepopulated **Forms** directory in your home directory
   
2. Run **jupyter noteboook** in your home directory
   * This will run a private jupyter notebook 
   
3. In the notebook navigate to the Forms directory and start the "Create_Submission_Form.ipynb" notebook
   * Follow the instructions
   
4. Have a look at the demo and documentation notebooks located in the **Forms/Doc** directory in your home     

