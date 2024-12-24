from PyPDF2 import PdfReader
from django.shortcuts import redirect, render,get_object_or_404
from UniWeb_13_024_7.forms import *
from UniWeb_13_024_7.models import *
from UniWeb_13_024_7.utils import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
# Create your views here.
import os



@login_required
def like_document(request,pdf_name,user_id,etat):
    if request.method == 'POST':
        user=get_object_or_404(User,pk=user_id)

        if Document.objects.filter(name=pdf_name).exists():
            pdf= Document.objects.get(name=pdf_name)
            pdf_like =DocumentLike.objects.get(user=user,document=pdf)
            type= 'document'
        else:
            pdf= Cours.objects.get(name=pdf_name)
            pdf_like =CoursLike.objects.get(user=user,cours=pdf)
            type= 'cours'

        if etat == 'like':
            pdf_like.like=True
            pdf_like.save()

            if type == 'document':
                compteur= DocumentLike.objects.filter(document=pdf,like=True).count()
            elif type == 'cours':
                compteur= CoursLike.objects.filter(cours=pdf,like=True).count()

            return JsonResponse({'compteur':str(compteur)})
        elif etat == 'dislike':
            pdf_like.like=False
            pdf_like.save()

            if type == 'document':
                compteur= DocumentLike.objects.filter(document=pdf,like=True).count()
            elif type == 'cours':
                compteur= CoursLike.objects.filter(cours=pdf,like=True).count()

            return JsonResponse({'compteur':str(compteur)})
        elif etat == 'neutre':

            if type == 'document':
                compteur= DocumentLike.objects.filter(document=pdf,like=True).count()
            elif type == 'cours':
                compteur= CoursLike.objects.filter(cours=pdf,like=True).count()

            if pdf_like.like == True:
                return JsonResponse({'etat': 'liker','compteur':str(compteur)})
            else:
                return JsonResponse({'etat': 'disliker','compteur':str(compteur)})
        


@login_required
def like_event(request,event_id,user_id,etat):
    if request.method=='POST':
        try:
            user= get_object_or_404(User,pk=user_id)
            event= Events.objects.get(pk=event_id)
            event_like= EventLike.objects.get(user=user,event=event)


            if etat == 'like':
                event_like.like=True
                event_like.save()

                compteur= EventLike.objects.filter(user=user,event=event,like=True).count()
                return JsonResponse({'compteur':str(compteur)})
            elif etat == 'dislike':
                event_like.like=False
                event_like.save()

                compteur= EventLike.objects.filter(user=user,event=event,like=True).count()
                return JsonResponse({'compteur':str(compteur)})
            elif etat == 'neutre':
                compteur= EventLike.objects.filter(user=user,event=event,like=True).count()
                if event_like.like == True:
                    return JsonResponse({'etat': 'liker','compteur':str(compteur)})
                else:
                    return JsonResponse({'etat': 'disliker','compteur':str(compteur)})
        except:
            return JsonResponse({})

@login_required
def FavorisGestion(request,pdf_name,user_id,etat):
    if request.method == 'POST':
        user= get_object_or_404(User,pk=user_id)

        if Document.objects.filter(name=pdf_name).exists():
            pdf= Document.objects.get(name=pdf_name)
            favoris= FavorisDocument.objects.get(user=user,pdf=pdf)
        else:
            pdf= Cours.objects.get(name=pdf_name)
            favoris= FavorisCours.objects.get(user=user,pdf=pdf)
    
        if etat == 'neutre':
            if favoris.favoris == True:
                return JsonResponse({'favoris': '1'})
            else:
                return JsonResponse({'favoris':'0'})
        else:
            if favoris.favoris == True:
                favoris.favoris=False
                favoris.save()
                return JsonResponse({'favoris':'0'})
            elif favoris.favoris == False:
                favoris.favoris= True
                favoris.save()
                return JsonResponse({'favoris':'1'})

@login_required
def read_view(request,pdf_name):
    try:
        if Document.objects.filter(name=pdf_name).exists():
            pdf= Document.objects.get(name=pdf_name)
        else:
            pdf= Cours.objects.get(name=pdf_name)
    except:
        return redirect('main:error',message='PDF Introuvable',lien='main:compte')
    return render(request,'main_html/account/favoris.html',{'pdf':pdf})









def index_view(request):
   return render(request,'main_html/index.html',{})

def cours_view(request):
    user= request.user
    cours= Cours.objects.filter(publier=True).order_by('id')
    filiere= Filiere.objects.all()
    level= NiveauEtude.objects.all()

    search_content= request.GET.get('search')
    option= request.GET.get('options')
    champs=['name','university']
    if search_content is not None and search_content != '':
        if not option in champs:
            return redirect('main:error',message='Veuillez définir un critère valide',lien='main:cours')
        try:
            filter= {f"{option}__icontains":search_content}
            cours= Cours.objects.filter(**filter)
        except:
            return redirect('main:error',message='Votre recherche est incorrecte',lien='main:cours')


    if user.is_authenticated:
        cours_trier=[]
        i=0
        for objet in cours:
            if objet.level == user.profil.level and objet.filiere == user.profil.filiere:
                cours_trier.insert(i,objet)
                i+=1
            elif objet.level == user.profil.level or objet.filiere == user.profil.filiere:
                cours_trier.insert(i,objet)
                i+=1
            else:
                cours_trier.append(objet)
                
        cours=cours_trier

    pagination= Paginator(cours,26)
    page= request.GET.get('page')
    cours= pagination.get_page(page)

    if request.method  == 'POST':
        form= AddCour(request.POST, request.FILES)

        try:
            if form.is_valid():
                form.full_clean()
                cour= form.save(commit=False)

                if user.is_authenticated:
                    cour.publier_par = user 
                
                try:
                    cour.save()
                except ValidationError as e:
                    error= e.message_dict
                    if error.get('error_cour_1'):
                        return redirect('main:error',message='Ce cours est déja disponible',lien='main:cours')
                    elif error.get('error_cour_2'):
                        return redirect('main:error',message=error.get('error_cour_2')[0],lien='main:cours')
                    elif error.get('error_cour_3'):
                        return redirect('main:error',message=error.get('error_cour_3')[0],lien='main:cours')

                alerte_admin_email(user.username,cour.name)
                return redirect('main:exo_redirect',lien='main:cours')
        except:
            return redirect('main:error',message='Nous avons rencontrer un probleme avec votre fichier',lien='main:cours')

    else:
        form= AddCour()

                
    return render(request,'main_html/cours.html',{'form': form,'elements':cours,'filiere': filiere,'levels':level})


def exo_view(request):
    user= request.user
    filiere= Filiere.objects.all()
    level= NiveauEtude.objects.all()
    exercices= Document.objects.filter(publier=True).order_by('id')

    # syteme de traitement pour le formulaire
    search_content= request.GET.get('search')
    option= request.GET.get('option')
    champs=['name','sujet','exercice','TD']

    if search_content is not None and search_content != "":
        if not option in champs:
            return redirect('main:error',message='Veuillez définir un critère valide',lien='main:exo')
        try:
            if option =='sujet' or option == 'exercice' or option == 'TD':
                list1=TypeOf.objects.get(name__icontains=option)
                exercices= list1.type.filter(name__icontains=search_content)
            else:
                filter= {f"{option}__icontains":search_content}
                exercices= Document.objects.filter(**filter)
        except:
            return redirect('main:error',message='Votre recherche est incorrecte',lien='main:exo')
        

    # systeme de tries si l'utilisateur est connecter
    if user.is_authenticated:
        exercices_trier=[]
        i=0
        for objet in exercices:
            if objet.level == user.profil.level and objet.filiere == user.profil.filiere:
                exercices_trier.insert(i,objet)
                i+=1
            elif objet.level == user.profil.level or objet.filiere == user.profil.filiere:
                exercices_trier.insert(i,objet)
                i+=1
            else:
                exercices_trier.append(objet)
                
        exercices=exercices_trier

    paginator= Paginator(exercices,26)
    page_number= request.GET.get('page')
    exercices= paginator.get_page(page_number)

    if request.method == 'POST':
        form= AddPDF(request.POST, request.FILES)

        try:
            if form.is_valid():                
                form.full_clean()
                exo= form.save(commit=False)

                if user.is_authenticated:
                    exo.publier_par= user
                    username= user.username
                filename= exo.file.name

                try:
                    exo.save()
                except ValidationError as e:
                    error= e.message_dict
                    if error.get('error_document_1'):
                        return redirect('main:error',message='Cet exercice ou sujets est déja disponible.',lien='main:exo')
                    elif error.get('error_document_2'):
                        return redirect('main:error',message=error.get('error_document_2')[0],lien='main:exo')
                    elif error.get('error_document_3'):
                        return redirect('main:error',message=e.message_dict.get('error_document_3')[0],lien='main:exo')
                    elif error.get('error_document_4'):
                        return redirect('main:error',message=error.get('error_document_4')[0],lien='main:exo')
                    elif error.get('error_document_5'):
                        return redirect('main:error',message=e.message_dict.get('error_document_5')[0],lien='main:exo')
                    
                alerte_admin_email(username,filename)

                return redirect('main:exo_redirect',lien='main:exo')
        except:
            return redirect('main:error',message='Nous avons rencontrer un probleme avec votre fichier',lien='main:exo')
    else:
        form= AddPDF()

    return render(request,'main_html/exo.html',{'elements':exercices,'form':form,'filiere':filiere,'levels':level})

@login_required
def single_pdf_view(request,name): # pour voir le pdf avec plus d'information
    user= request.user
    try:
        if Document.objects.filter(name=name).exists():
            pdf= Document.objects.get(name=name)

            #like
            if not DocumentLike.objects.filter(user=user,document=pdf).exists():
                DocumentLike.objects.create(user=user,document=pdf)

            #favoris
            if not FavorisDocument.objects.filter(user=user,pdf=pdf).exists():
                FavorisDocument.objects.create(user=user,pdf=pdf)

            lien='main:exo'

        else:
            pdf= Cours.objects.get(name=name)

            #like
            if not CoursLike.objects.filter(user=user,cours=pdf).exists():
                CoursLike.objects.create(user=user,cours=pdf)

            #favoris
            if not FavorisCours.objects.filter(user=user,pdf=pdf).exists():
                FavorisCours.objects.create(user=user,pdf=pdf)


            lien='main:cours'

        auteur= PdfReader(pdf.file).metadata.author
    except:
        return redirect('main:error',message='PDF Introuvale',lien='main:index')

    return render(request,'main_html/pdf.html',{'pdf':pdf,'lien':lien,'auteur':auteur})









def filter_view_exo(request,name):
    #filtre-exos
    try:
        filiere= Filiere.objects.all()
        level= NiveauEtude.objects.all()
        if Filiere.objects.filter(name=name).exists():
            filtre= Filiere.objects.get(name=name)
            exercices= filtre.filiere.all()
        else:
            filtre= NiveauEtude.objects.get(name=name)
            exercices= filtre.level.all()
    except:
        exercices=None
    #filtre

    lien='main:exo'
    filter_lien='main:filtre'
    return render(request,'main_html/filtre.html',{'elements':exercices,'filiere':filiere,'levels': level,'lien':lien,'filtre':filter_lien})

def filter_view_cours(request,name):
    #filtre-cours
    filiere= Filiere.objects.all()
    level= NiveauEtude.objects.all()
    try:
        if Filiere.objects.filter(name=name).exists():
            filtre= Filiere.objects.get(name=name)
            cours= filtre.filiere_cours.all()
        else:
            filtre= NiveauEtude.objects.get(name=name)
            cours= filtre.level_cours.all()
    except:
        cours= None
    #filtre

    lien='main:cours'
    filter_lien='main:filtre_cours'
    return render(request,'main_html/filtre.html',{'elements':cours,'filiere':filiere,'levels': level,'lien':lien,'filtre':filter_lien})










# vue de telechargement
from django.conf import settings
from django.http import FileResponse

def download(request,objet_type,objet_id):
        try:
            if objet_type == 'Document':
                objet= Document.objects.get(pk=objet_id)
                if os.path.exists(objet.file.path):
                    objet.downloads +=1
                    objet.save()
                    return FileResponse(open(objet.file.path, 'rb'),as_attachment=True,filename=f'Correction_{objet.file.name}')
            elif objet_type == 'Correction':
                objet= Document.objects.get(pk=objet_id)
                if os.path.exists(objet.correction.path):
                    return FileResponse(open(objet.correction.path, 'rb'),as_attachment=True,filename=objet.correction.name)
            elif objet_type == 'Cours':
                objet= Cours.objects.get(pk=objet_id)
                if os.path.exists(objet.file.path):
                    objet.downloads += 1
                    objet.save()
                    return FileResponse(open(objet.file.path, 'rb'),as_attachment=True,filename=objet.file.name)
            elif objet_type == 'Events':
                objet= Events.objects.get(pk=objet_id)
                if os.path.exists(objet.file.path):
                    objet.downloads += 1
                    objet.save()
                    return FileResponse(open(objet.file.path, 'rb'),as_attachment=True,filename=objet.file.name)

        except Exception:
                return redirect('main:download_redirect')









def events_view(request):
    events= Events.objects.all()
    return render(request,'main_html/events.html',{'events':events})

def event_details(request,event_name):
    event= Events.objects.get(name=event_name)
    user= request.user

    if user.is_authenticated:
        if not EventLike.objects.filter(user=user,event=event).exists():
            EventLike.objects.create(user=user,event=event)

    return render(request,'main_html/event_page.html',{'event':event})







#  TRAITEMENT DES UTILISTEURS

@login_required
def compte_view(request): # vue de la page compte et mise a jour de l'avatar
    name= request.user.username[0] # nessecaire pour la creation du profil par defaut
    profile, create= Profil.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form= Avatar(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main:compte')
    else:
        form= Avatar()

    user= request.user

    favoris=[]
    favoris.append(FavorisDocument.objects.filter(user=user,favoris=True))
    favoris.append( FavorisCours.objects.filter(user=user,favoris=True))

    if user.is_superuser or user.is_staff:

        cours_like= CoursLike.objects.filter(like=True).count()
        document_like= DocumentLike.objects.filter(like=True).count()
        event_like= EventLike.objects.filter(like=True).count()

        all_cours= Cours.objects.all()
        cours_download=0
        for i in all_cours:
            cours_download += i.downloads

        all_document= Document.objects.all()
        document_download=0
        for i in all_document:
            document_download += i.downloads

        all_event= Events.objects.all()
        event_download=0
        for i in all_event:
            event_download += i.downloads

    context={
        'form': form,
        'name':name,
        'cours_like':cours_like,
        'document_like':document_like,
        'event_like': event_like,
        'cours_download':cours_download,
        'document_download':document_download,
        'event_download': event_download,
        'favoris': favoris,
        }

    return render(request, 'main_html/account/compte.html',context)

@login_required
def update_view(request,username): # mise a jour des champs bio,universite,cycle,filiere
    user= User.objects.get(username=username)
    profile= Profil.objects.get(user=user)
    if request.method == 'POST':
        bioform= Bio(request.POST,instance=profile)
        if bioform.is_valid():
            bioform.save()
            return redirect('main:compte')
        else:
            return redirect('main:error',message='assurez-vous que les données sont valides',lien='main:compte')
    else:
        bioform= Bio(instance=profile)

    return render(request,'main_html/account/update_profile.html',{'bioform':bioform})

@login_required
def remove_view(request,username): # suppression de l'avatar
    user= get_object_or_404(User,username=username)
    profil= Profil.objects.get(user=user)
    if profil.image:
        profil.image.delete(save=True)
        profil.save()
    return redirect('main:compte')

@login_required
def delete_view(request,username): # suppression du compte
    user= User.objects.get(username=username)
    profile= Profil.objects.get(user=user)
    try:
        if profile.image:
            profile.image.delete()
        user.delete()
        return redirect('main:success_delete')

    except:
        return redirect('main:error',message='Réessayer ultérieurement',lien='main:index')


def login_views(request): # vue de connexion
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('main:compte',)
        else:
            messages.info(request,"Données incorrect")

    form= AuthenticationForm(request.POST)
    return render(request,'main_html/account/login.html',{'form': form,})

def sigin_views(request): # vue de la page de creation de compte
    if request.method == 'POST':
        form= SiginForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            email= form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                return redirect('main:error',message='un utilisateur avec cet email existe déja',lien='main:sigin')
            form.save()
            user= authenticate(username=username,password=password)
            login(request,user)
            Profil.objects.create(user=user)
            return redirect('main:compte')
        else:
            return redirect('main:error',message='assurez-vous que les données sont valides',lien='main:sigin')#('main:sigin2_redirect')
    else:
        form= SiginForm()

    return render(request, 'main_html/account/sigin.html',{'form':form})

@login_required
def logout_views(request): # vue de deconnexion
    logout(request)
    return redirect('main:index')

# Traitement du changement de mot de passe
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def SendChangepassword_view(request):
    if request.method == 'POST':
        form= Password_Email(request.POST)
        if form.is_valid():
            email= form.cleaned_data['email']
            try:
                user= User.objects.get(email=email)
            except:
                user= None
            
            if user is not None:

                subject='UniWeb Modification du mot de passe'
                context={
                    'username': user.username,
                    'url_site': get_current_site(request).domain,
                    'uid64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' # mettez le prtocole en https en production
                }
                email_html= render_to_string('main_html/email_template/password_email.html',context)
                email_brute= strip_tags(email_html)
                message= EmailMultiAlternatives(subject,email_brute,'',[str(email)])
                message.attach_alternative(email_html,'text/html')
                message.send()
                return redirect('main:email_redirect')
            
            else:
                return  redirect('main:error', message="assurez-vous que votre email est celui de votre connexion", lien='main:index')

        else:
            # logique en cas d'erreur
            return redirect('main:error', message="assurez-vous que votre email est valide",lien='main:index')
    else:
        form= Password_Email()

    return render(request,'main_html/account/ask_email.html',{'form':form})

    # return render(request,'main_html/email_template/password_email.html',context)

def newPassword_view(request,uid64,token):
    user_id= force_str(urlsafe_base64_decode(uid64))
    user= User.objects.get(pk=user_id)
    if user is not None and default_token_generator.check_token(user,token):
        if request.method == 'POST':
            form= SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                request.session.cycle_key()
                return redirect('main:compte')
            else:
                return redirect('main:error', message='assurez-vous que les données sont valides',lien='main:index')
        else:
                form= SetPasswordForm(user)

    return render(request,'main_html/account/newpassword.html',{'form':form})

# Traitement du changement de mot de passe

#  TRAITEMENT DES UTILISTEURS








# vue de redirection

def exo_redirect(request,lien):
    url= 'assets/icone/email.png'

    context={
        'image':url,
        'subject':  'PDF ajouter avec succès'.capitalize(),
        'message':'Un email a été envoyer aux administrateurs pour valider votre PDF, <br> Nous vous remercions.',
        'lien':lien
    }
    return render(request,'main_html/state.html',context)

def sujet_redirect(request):
    url= 'assets/icone/email.png'

    context={
        'image':url,
        'subject':  'Sujet ajouter avec succès'.capitalize(),
        'message':'un email a été envoyer aux administrateurs pour valider votre sujet'.capitalize()
    }
    return render(request,'main_html/state.html',context)


def success_delete(request):
    url= 'assets/icone/supprimer.png'

    context={
        'image':url,
        'subject':   'compte supprimer avec succès'.capitalize(),
        'message':''
    }
    return render(request,'main_html/state.html',context)


def email_redirect(request):
    url= 'assets/icone/email.png'

    context={
        'image':url,
        'subject':  'Email envoyer avec succès'.capitalize(),
        'message': 'veuillez vérifier votre boîte à email pour continuer'.capitalize()
    }
    return render(request,'main_html/state.html',context)


def download_error(request):
    url= 'assets/icone/error.png'

    context={
        'image':url,
        'subject':  "une erreur s'est produite".capitalize(),
        'message':''
    }
    return render(request,'main_html/state.html',context)

def error_view(request,message,lien):
    url= 'assets/icone/error.png'

    context={
        'image':url,
        'subject':  "une erreur s'est produite".capitalize(),
        'message': message.capitalize(),
        'lien':lien
    }
    return render(request,'main_html/state.html',context)

def validation_view(request,subject,message):
    url= 'assets/icone/valider.png'

    context={
        'image':url,
        'subject':  subject.capitalize(),
        'message': message.capitalize()
    }
    return render(request,'main_html/state.html',context)

# vue de redirection

# VUE POUR LE CHARGEMENT DYNAMIQUE
# def paginator_view_for_document(request):
#     exercice= Document.objects.all()
#     page= request.GET.get('page')
#     paginator= Paginator(exercice,page_par_pagination)
#     content= paginator.get_page(page)

#     return render(request, 'main_html/test.html',{'new_elements':content})

