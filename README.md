# FormFabric: data submission workflow support components 

a data submission workflow normally is based on the following steps:
* information collection to manage the specific data ingest request
* data ingest
* data quality assurance
* data publication (making data accessible in file system or via portals)
* data archival 

FormFabric provides:
* interactive ipython notebooks for data submission related information collection 
* a set of utilities to store and manage submission information (json based)
* a set of utilities for data managers to manage submission related information based on json as well as an object representation of json information. 
* a tranformation of this information to a W3C Prov representation (xml, json as well as graph)


## Installation

* Dependencies:
   * a python 3 installation with ipython and jupyter notebook support
   * a conda based python (3.x) installation (https://www.continuum.io/downloads) is recommended 
   * conda dependencies: conda install ipython, notebook
   * pip dependencies (will be automatically installed): 'gitpython', 'prov'
      
        
* git clone https://github.com/IS-ENES-Data/submission_forms.git
* cd ..your_installation_path/submission_forms.git 
* pip install . 
     * this installs also the dependencies 'gitpython' and 'prov'

* see documention

## Usage

* see tutorial and demo notebooks in the "turorial" and "test" directories
