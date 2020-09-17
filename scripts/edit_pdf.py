# -*- coding: utf-8 -*-

import pdfrw
from reportlab.pdfgen import canvas
from datetime import date
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont 
import os


pdfmetrics.registerFont(TTFont('Hebrew', 'ArialHB.ttf'))


def create_overlay(child):  
    today = date.today()
    today_str = today.strftime("%d/%m/%Y")  
    health_canvas = canvas.Canvas(child.child_id + "_overlay.pdf")
    health_canvas.setFont("Hebrew", 14)
    
    health_canvas.drawString(395, 548, get_display(child.child_name))
    health_canvas.drawString(280, 548, get_display(child.child_id))
    
    health_canvas.drawString(450, 402, get_display(child.parent_name))
    health_canvas.drawString(330, 402, get_display(child.parent_id))
    health_canvas.drawString(210, 402, today_str)
    
    health_canvas.save()

def merge_pdfs(child, output):   
    create_overlay(child)
    overlay_path = child.child_id + "_overlay.pdf"
    form_pdf = child.child_id + ".pdf"
    form = pdfrw.PdfReader("health_forms/" + form_pdf)
    olay = pdfrw.PdfReader(overlay_path)
    
    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()
    
    writer = pdfrw.PdfWriter()
    writer.write(output, form)

    if os.path.exists(overlay_path):
        os.remove(overlay_path)
