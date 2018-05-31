
# handler for rt interaction as well as json info db 

import sys
import base64
import rt
import ConfigParser
import io
from tinydb import TinyDB,Query
#from os import listdir, walk
import glob
import json


def get_info_db(info_directory):
    db = TinyDB(info_directory)
    return db

def db_get_name(db,myname):
    info = Query()
    sub_results = db.search(info.sub.last_name == myname)
    return sub_results
    
def db_get_ticket_info(db,ticket):
    info = Query()
    sub_results = db.search( info.sub.ticket_id == ticket) 
    #ing_results = db.search( info.sub.ticket_id == ticket) )
    #che_results = db.search( info.ing.ticket_id == ticket) )
    #pub_results = db.search( info.pub.ticket_id == ticket) ) 
    
    first_name = results[0].sub.first_name
    last_name= results[0].sub.last_name
    email = info.sub.email
    return sub_results, first_name,last_name, email


def summary_html(mylist):
        html = []
            
        html.append("<table width=100%>")
        html.append("<tr>")
        html.append("<td><b>form name<b></td>")
        html.append("<td><b>keyword<b></td>")
        html.append("<td><b>timestamp<b></td>")
        html.append("<td><b>model / exp<b></td>")   
        html.append("<td><b>status</td>")
        html.append("</tr>")
        
        for entry in mylist:
          #print entry['sub']
          html.append("<tr>")
          html.append("<td>{0}</td>".format(entry['sub']['form_name']))
          html.append("<td>{0}</td>".format(entry['sub']['keyword']))
          html.append("<td>{0}</td>".format(entry['sub']['timestamp']))
          html.append("<td>{0}</td>".format(entry['model_id']))
          html.append("<td>{0}</td>".format(entry['sub']['status']))
          html.append("</tr>")
        
        html.append("</table>")
        return ''.join(html)

    
rt_module_present = False
try:
   import rt
   rt_module_present = True
except ImportError as e:
   pass

def get_tracker(rt_pwd):
    tracker = rt.Rt('https://dm-rt.dkrz.de/REST/1.0/','kindermann',rt_pwd)
    tracker.login()
    return tracker

def rt_get_latest_message(tracker,message_id):
   messages = tracker.get_history(message_id)
   latest_message = messages[-1]['Content']
   return latest_message

def sync_info(remote_path, local_path):
   """ synchronise local with remote submission form git repo
   """
   pass


def rt_reply(tracker,message_id, rtext):
    tracker.reply(message_id, text=rtext)


    
