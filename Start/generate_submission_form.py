import os,sys,shutil,uuid


def generate_submission_form(my_first_name,my_last_name,my_email,my_project):
    ''' take project notebook template, rename it and copy the result to the 
        projects submission form directory as a personal copy for the end user
    '''
        #working_dir = os.getcwd()
    if my_project == "CORDEX":
           my_id = str(uuid.uuid1())
	   my_name = my_first_name+"_"+my_last_name
	   target_file_name=my_project+"__"+my_name+"__submission"+"__"+my_id+".ipynb"
 	   target = "../"+my_project+"/"+target_file_name
	   #print target

	   source_file_name = "Templates/"+my_project+"_submission_form.ipynb"
	   source = "../"+source_file_name
	   #print source
    
	   shutil.copyfile(source,target)
           print "--------------------------------------------------"
           print "submission form created, please visit the following link:"
           print "https://qc.dkrz.de:8080/tree/"+my_project+"/"+target_file_name
    else:
           print "--------------------------------------------------"
           print "currently only submission forms for the project \"CORDEX\" are supported"
           print "no submission form created"
           print "please re-evaluate cell with proper project information"
