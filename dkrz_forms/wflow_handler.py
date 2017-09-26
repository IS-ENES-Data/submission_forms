#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 16:46:24 2017

workflow handler: helper functions to update and process workflow forms

@author: stephan
"""
from datetime import datetime
from dkrz_forms import form_handler

def get_wflow_description(form):
    wflow_steps = {}
    for (short_name,long_name) in form.workflow:
        wflow_steps[long_name] = short_name
    return wflow_steps   

def rename_action(action,form):
    '''
    convinience function to map short names to lang wflow step namees"
    '''
    wflow_dict = get_wflow_description(form)
    if action not in list(wflow_dict.values()):
        if action in list(wflow_dict.keys()):
         action = wflow_dict[action]
        else:
            print("Error: wrong action name, should be one of: ",list(wflow_dict.values()))
    return action        
        

def start_action(action,form, my_name):
    
    action = rename_action(action,form)
    wflow_step = getattr(form,action)
 
    # set status messages:
    form.status = action
    wflow_step.activity.status ="1:in-progress"
    wflow_step.activity.error_status="0:open"
    wflow_step.entity_out.status="1:stored"
    wflow_step.entity_out.check_status="0:open"
    
    # set start information:
    wflow_step.agent.responsible_person = my_name
    wflow_step.activity.start_time = str(datetime.now())
    
    # store_info
    
    saved_form = form_handler.save_form(form,my_name+": " + action +" started")
    return saved_form



def update_action(action,form, my_name):
    action = rename_action(action,form)
    wflow_step = getattr(form,action)
    
    saved_form = form_handler.save_form(form,my_name+": " + action + " updated")
    return saved_form


def finish_action(action,form, my_name,review_report):
    action = rename_action(action,form)
    wflow_step = getattr(form,action)
    
    
    wflow_step.activity.status ="4:closed"
    wflow_step.activity.error_status="1:ok"
    wflow_step.entity_out.status="1:stored"
    wflow_step.entity_out.check_status="3:ok"
    
     
    wflow_step.activity.end_time = str(datetime.now())
    wflow_step.activity.timestamp = str(datetime.now())
    
    saved_form = form_handler.save_form(form,my_name+": " + action + " finished")
    return saved_form 


    