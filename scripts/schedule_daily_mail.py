import schedule
import time
import json
import os

from send_email import send_email
from edit_pdf import create_overlay, merge_pdfs
from collections import namedtuple
from datetime import date

class Student(object):
    def __init__(self, name, email, bcc_email, file_name, *args, **kwargs):
        self.name = name
        self.email = email
        self.bcc_email = bcc_email
        self.file_name = file_name

def get_names_from_json():
    stds=[]
    with open('json_files/mail_list.json') as f:
        data = json.load(f)
        for st in data["names"]:
            stds.append(Student(**st))
    
    return stds

def job():
    if date.today().weekday() == 5 : return

    create_overlay()
    all_names = get_names_from_json()
    overlay_file = 'date_overlay.pdf'
    
    for nm in all_names:
        output_file_name= "health_forms/" + nm.file_name + "_date.pdf"
        merge_pdfs(nm.file_name + ".pdf", 
                overlay_file, 
                output_file_name)

        send_email(nm.name, nm.email,nm.bcc_email, output_file_name)
        
        print ("Mail sent for: " + nm.name + " To: " +nm.email)
        
        if os.path.exists(output_file_name):
            os.remove(output_file_name)
    
    if os.path.exists(overlay_file):
            os.remove(overlay_file)
    return


if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    print ("- - - Job Started - - -")
    schedule.every().day.at("08:00").do(job)
    

    while True:
        schedule.run_pending()
        time.sleep(60) # wait one minute
