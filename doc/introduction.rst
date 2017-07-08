
Introduction
=================


Data delivery to a data center and data ingest management at a data center are complex activities requiring complex documentation and communication. 

Normally the following generic workflow is followed:

* A) data ingest request from the data provider (end user) to data center
* B) data ingest request evaluation at data center and communication with end user to organize data delivery
* C) data transport (push or pull using various tools) to data center
* D) data quality control at data center (completeness, correctnes with specific requirements, etc.)
* E) data import and publication at data center (import in some kind of data store - with associated metadata, publication to a portal interface, e.g. ESGF), often this includes the assignment of persistent identifiers (PIDs) to the data objects
* F) data archival and data citation

This generic workflow has to be adapted to the specific needs of specific data projects.
Additionally this workflow is normally not linear, but includes backtrack loops e.g. in cases where errors are detected at a data center and data needs to be corrected, deleted and updated. 

Static data ingest solutions building upon e.g. a set of fixed online forms and fixed internal data management steps thus are often too unflexible and heavy weight (e.g. with respect to implementation, deployment, documentation, associated user training, etc.). 

The approach taken here wants to:

* provide simple, quick and easy interaction forms between data center and data provider based on jupyter notebook interfaces

   * these forms can either be served at the data center to provide web accessible interactive interfaces for information collection,
   * these forms also can be run client-side (data provider side) - the completed forms are sent to the data center in this case
      
* provide a generic, simple serialization format for the information related to a data ingest activity (based on json)
* provide a generic provenance based structuring of this information based on the W3C PROV standard
* provide simple python code snippets, libraries and tools data managers can use to enrich and modify data ingest related information (e.g. add quality assurance reports, data publication reports etc.)
* (a generic persistance layer for storing data ingest related information as well as searching this information is on the todo list)  

The goal is to establish stepwise a growing set of data ingest helper packages, wich can be used to support current and future data projects and their data ingest management needs.

Please see the tutorial and installation sections for applications examples.

