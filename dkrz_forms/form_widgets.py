# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:27:28 2017

@author: stephan
"""

from ipywidgets import widgets
from IPython.display import display, Javascript

align_kw = dict(
    _css = (('.widget-label', 'min-width', '20ex'),),
    margin = '0px 0px 5px 12px'
)

def ask():
    global LAST_NAME, FIRST_NAME, EMAIL, KEY, PROJECT
    LAST_NAME = widgets.Text(value="",description="Your last name: ",width=200, **align_kw)
    FIRST_NAME = widgets.Text(value="",description="Your first name: ",width=200, **align_kw)
    EMAIL = widgets.Text(value="", description="    Your email:",width=200, **align_kw)
    PROJECT = widgets.Dropdown(description = "Project selection: ", options=["CORDEX","CMIP6","DKRZ_CDP","test"],**align_kw)
    KEY = widgets.Text(value="", description="A key to identifiy your form: ",width=120,**align_kw)
    
    display(LAST_NAME)
    display(FIRST_NAME)
    display(EMAIL)
    display(KEY)
    display(PROJECT)

    #def handle_submit(sender):
    #    print LAST_NAME.value
     #   print FIRST_NAME.value

  #  LAST_NAME.on_submit(handle_submit)
  #  FIRST_NAME.on_submit(handle_submit)
  