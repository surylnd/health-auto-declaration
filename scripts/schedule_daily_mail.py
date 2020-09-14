import schedule
import time
import json
import os
import logging

from send_email import send_email
from edit_pdf import create_overlay, merge_pdfs
from collections import namedtuple
from datetime import date
from child import Child
from bidi.algorithm import get_display

def init():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))

    logging.basicConfig(level=logging.INFO,filename=date.today().strftime("%d%m%Y") + 'send_mails.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("- - - Job Started - - -")

def get_children_from_json():
    children=[]
    with open('json_files/mail_list.json') as f:
        data = json.load(f)
        for child_json in data["names"]:
            children.append(Child(**child_json))
    
    return children

def job():
    if date.today().weekday() == 5 : return
    
    all_children = get_children_from_json()
    
    for child in all_children:
        logging.info(f'Found {get_display(child.child_name)} info')
        if child.send_email:
            output_file_name= "health_forms/" + child.child_id + "_date.pdf"
            merge_pdfs(child, output_file_name)

            send_email(child, output_file_name)
            
            logging.info(f'Mail sent for: {get_display(child.child_name)} To: {child.email}')
            
            if os.path.exists(output_file_name):
                os.remove(output_file_name)   
        else:
            logging.info(f'Mail NOT sent for: {get_display(child.child_name)}')
    return


if __name__ == '__main__':
    init()
    schedule.every().day.at("07:30").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)
