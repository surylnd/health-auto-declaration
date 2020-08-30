import pdfrw
from reportlab.pdfgen import canvas
from datetime import date

def create_overlay():    
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    
    c = canvas.Canvas('date_overlay.pdf')
    c.drawString(210, 402, d)
    c.save()

def merge_pdfs(form_pdf, overlay_pdf, output):   
    form = pdfrw.PdfReader("health_forms/" + form_pdf)
    olay = pdfrw.PdfReader(overlay_pdf)
    
    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()
        
    writer = pdfrw.PdfWriter()
    writer.write(output, form)
