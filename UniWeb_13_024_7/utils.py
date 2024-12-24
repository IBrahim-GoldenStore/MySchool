from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.core.files import File
from PyPDF2 import PdfReader
from io import BytesIO
import unicodedata
from PIL import Image
import hashlib
import re

def normalize_name(name:str):
    without_pdf= name.replace('.pdf','')
    without_accents= unicodedata.normalize('NFKC',without_pdf).encode('ascii','ignore').decode('utf-8')
    without_special_caractere= re.sub(r'[^\w\s-]','_',without_accents)
    without_espace= without_special_caractere.replace(" ","_")

    return without_espace

def compressor(comp_image=None,filename:str=None):
        img= Image.open(comp_image)
        img= img.convert('RGB')
        img.thumbnail((500,500))
        format='webp'
        img_io= BytesIO() # creer un buffer
        img.save(img_io, format=format,quality=80) # sauvegarde limage dans le buffer
        img_io.seek(0)
        img_file= File(img_io, name=filename+'_'+comp_image.name[0:6]+'.'+format)
        return img_file


def alerte_admin_email(username:str,filename:str):
    email_recevers= User.objects.filter(is_staff=True).values_list('email',flat=True)
    email= render_to_string('main_html/email_template/send_email.html',{'username':username,'filename':filename})

    email_whitout_tags= strip_tags(email)
    message= EmailMultiAlternatives(
        'Nouveau fichier partager',
        email_whitout_tags,
        '',
        list(email_recevers)
    )
    message.attach_alternative(email,'text/html')
    message.send()

def make_hash(file):
    if file:
        hasher= hashlib.blake2b(digest_size=16)
        pdf = PdfReader(file) # Notez que la lecture des textes avec pdfreader n'inclus pas les annotations
        for page in pdf.pages: # d'ou son utilisations ici car cela garantit un hash uniforme pour tout les pdfs
            # if page.extract_text():
                hasher.update(page.extract_text().encode('utf-8'))

        return hasher.hexdigest()

        # for chunk in file.chunks():
        #     hasher.update(chunk)
        # return hasher.hexdigest()
    # else:
    #     return None

# EN ESSAI
# import fitz

# def couverture(file):
#     doc= fitz.open(stream=file.read(),filetype='pdf')
#     page= doc[0]
#     page=page.get_pixmap()
#     return File(page.samples)
