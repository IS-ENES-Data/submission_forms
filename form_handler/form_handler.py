# submission form jupyter notebook supporting code
# Author: S. Kindermann
# Version: 0.1 (Dezember 2015) 
# to do:
# separate out generic form code (e.g. git repo handling) as a super class
# from which specific form handlers inherit

import os
from datetime import datetime
from git import Repo
join = os.path.join
import smtplib
from email.mime.text import MIMEText

class cordex_submission_form(object):

        sd = {}
	def __init__(self):
            
            self.first_name = ""
            self.last_name = ""
            self.email = ""
            self.submission_type = ""
            self.institution = ""
            self.institute_id = ""
            self.model_id = ""
            self.experiment_id = ""
            self.time_period = ""
            self.example_file_name = ""
            self.grid_mapping_name = ""
            self.grid_as_specified_if_rotated_pole = ""
            self.data_qc_status = ""
            self.data_qc_comment = ""
            self.terms_of_use = ""
            self.directory_structure = ""
            self.data_path = ""
            self.data_information = ""
	    self.exclude_variables_list = ""
	    self.variable_list_day = ""
	    self.variable_list_mon = ""
	    self.variable_list_sem = ""
	    self.variable_list_fx = ""
	    self.uniqueness_of_tracking_id = ""
            self.check_status="not checked"
            ## to-do: parameterize repo location or make it configurable easyly..
            ## 


	def cordex_file_info(self,file_name):
          # cordex file structure:
          # VariableName_Domain_GCMModelName_CMIP5ExperimentName_CMIP5EnsembleMember_RCMModelName_RCMVersionID_Frequency[_StartTime - EndTime].nc
	    cordex_template=["VariableName","Domain","GCMModelName","CMIP5ExperimentName","CMIP5EnsembleMember","RCMModelName","RCMVersionID","Frequency","TimeRange"] 
	    cordex_example = "tas_EUR-44_MPI-M-MPI-ESM-LR_historical_r1i1p1_CLMcom-CCLM4-8-17_v1_day_19710101-19751231.nc"
	    cordex_example_parts = cordex_example.split("_") 
	    for i,part in enumerate(cordex_example_parts):
    		print cordex_template[i],":",part


        def check_submission(self):
            ## to_do: add consistency checks 
            if not self.first_name:
               print "Please provide your first name"
               self.check_status="uncomplete"
            if not self.last_name:
               print "Please provide your last name"
               self.check_status="uncomplete" 

            if not self.check_status=="uncomplete":
               print "submission form for user "+self.first_name+" "+self.last_name+": check ok"
               self.check_status="complete_1"
            else:
               print "please correct errors before proceeding"

        def check_form_name(self,form_name):
            if form_name != "...":
                print "form name looks ok"
            else:
                print "Please fill in the form name for this document"

        def form_save(self):
            self.repo.git.add(all=True)
            self.repo.git.commit(message='Submission form for user '+self.first_name+"_"+self.last_name+' saved in git repository')
            print "submission form stored in local repository "


        def email_form_info(self):
            m_part1 = "You edited and saved a CORDEX submission form\n"
            m_part2 = "This form is accessible at: \n"
            m_part3 = "https://qc.dkrz.de:8080/notebooks/CORDEX/"+self.form_name+".ipynb \n"
            m_part4 = "to officially submit this form to be processed by DKRZ please follow the instructions in the submission part of the form \n"
            m_part5 = "in case of problems please contact data@dkrz.de"
            my_message = m_part1 + m_part2 + m_part3 + m_part4 + m_part5
            msg = MIMEText(my_message)
            msg['Subject'] = 'Your CORDEX data submission form'
            msg['From'] = "data_submission@dkrz.de"
            msg['To'] = self.email
            # Send the message via the qc VM SMTP server, but don't include the\n"
            # envelope header.\n",
            s = smtplib.SMTP('localhost')
            s.sendmail("data_submission@dkrz.de", ["kindermann@dkrz.de"], msg.as_string())
            s.quit()

        def form_submission(self):
            m_part1 = "A CORDEX data submission was requested by: " + self.first_name + " " + self.last_name + "\n" 
            m_part2 = "Corresponding email: "+ self.email +"\n"
            m_part3 = "Submission form url: https://qc.dkrz.de:8080/notebooks/CORDEX/"+self.form_name+".ipynb \n"
            m_part4 = "The submission is commited to the CORDEX submission form git repository with the name "+self.form_name +"\n"
            m_part5 = "Time of submission:"+ str(datetime.now())

            my_message = m_part1 + m_part2 + m_part3 + m_part4 + m_part5
            msg = MIMEText(my_message)
            msg['Subject'] = 'Test email from DKRZ data submission form management software - please ignore'
            msg['From'] = "data_submission@dkrz.de"
            msg['To'] = self.email
            msg['CC'] = "kindermann@dkrz.de"
            # Send the message via the qc VM SMTP server, but don't include the\n"
            # envelope header.\n",
            s = smtplib.SMTP('localhost')
            s.sendmail("data_submission@dkrz.de", ["kindermann@dkrz.de"], msg.as_string())
            s.quit()

          #  origin = repo.remotes.origin
          #  origin.push()
          #  print "Data submission form sent"
          #  print "A confirmation message will be sent to you"


sf = cordex_submission_form()
# initialize form object with location of git repo where submission forms are stored (locally)
sf.repodir='/home/dkrz/k202015/submission_forms/CORDEX'
sf.repo = Repo(sf.repodir)           

print "Submission form intitialized"
print "(technically a submission form (sf) object as well as a repository (repo object) are created to store the submission form)"
