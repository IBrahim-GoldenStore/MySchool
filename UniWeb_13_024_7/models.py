from PyPDF2 import PdfReader

from django.db import models

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from UniWeb_13_024_7.utils import *
from django.core.exceptions import ValidationError

from django.dispatch import receiver
from django.db.models.signals import pre_save,pre_delete


# Create your models here.

class Events(models.Model):
    name= models.CharField(max_length=50,verbose_name='Nom',unique=True,)
    apercu_rapide= models.CharField(max_length=100,verbose_name='Aperçue rapide',unique=True)
    description= models.CharField(max_length=5000,verbose_name='Description',unique=True)
    source= models.CharField(max_length=30,verbose_name='Source',unique=False,null=True,blank=True)
    image= models.ImageField(upload_to='./event_image',verbose_name='Image',null=True,blank=True,unique=True)
    add_date= models.DateTimeField(auto_now_add=True)
    file= models.FileField(upload_to='./events_file',verbose_name="fichier de l'evenement",null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    downloads= models.PositiveIntegerField(verbose_name='Telechargement',default=0,unique=False,null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name="#4-Évenement"
        verbose_name_plural="#4-Évenements"

class TypeOf(models.Model):
    name= models.CharField(max_length=30,verbose_name='type',unique=True,null=True,blank=True,default='')

    class Meta:
        verbose_name="Type"
        verbose_name_plural="Types"

    def __str__(self):
        return self.name

class Filiere(models.Model):
    sigle= models.CharField(max_length=15,verbose_name='Sigle',null=True,default='')
    name= models.CharField(max_length=100,verbose_name='Filière',unique=True,blank=True,null=True,default='')

    class Meta:
        verbose_name='Filière'
        verbose_name_plural='Filières'


    def __str__(self):
        return self.sigle
    
    
class NiveauEtude(models.Model):
    name=  models.CharField(max_length=30,verbose_name="Niveau d'étude",unique=True,null=True,default='')

    class Meta:
        verbose_name="Niveau d'étude"
        verbose_name_plural="Niveaux d'études"
    def __str__(self):
        return self.name

class Profil(models.Model):
    user= models.OneToOneField(User,on_delete= models.CASCADE)
    status= models.CharField(max_length=12,verbose_name='Status',default='Etudiant',null=True,blank=True)
    university= models.CharField(max_length=70,verbose_name='Universite',null=True,blank=True,default='Non définie')
    filiere= models.ForeignKey(Filiere,on_delete=models.CASCADE,verbose_name='Filière',null=True,blank=True,default="")
    level= models.ForeignKey(NiveauEtude,on_delete=models.CASCADE,verbose_name="Niveau d'étude",null=True,blank=True,default='')
    image= models.ImageField(upload_to='./avatar_profil',blank=True,null=True)
    bio= models.CharField(max_length=255,verbose_name="Biographie",null=True,blank=True,default="....Mon Biographie")

    class Meta:
        verbose_name='#1-Profile'
        verbose_name_plural='#1-Profiles'
        

    def __str__(self):
        return self.user.username


class Cours(models.Model):
    name=models.CharField(max_length=100,verbose_name="Nom",null=True,blank=True,unique=True)
    university= models.CharField(max_length=200,verbose_name="Université",null=True,blank=True)
    file= models.FileField(upload_to="./cours",verbose_name='fichier',validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    hash= models.CharField(max_length=64,unique=True,null=True,blank=True)

    filiere= models.ForeignKey(Filiere,on_delete=models.CASCADE,verbose_name='Filière',null=True,blank=True,default="",related_name='filiere_cours')
    level= models.ForeignKey(NiveauEtude,on_delete=models.CASCADE,verbose_name="Niveau du cours",null=True,blank=True,default='',related_name='level_cours')

    publier= models.BooleanField(verbose_name="Publier le fichier",default=False)
    publier_par= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    add_date= models.DateTimeField(auto_now_add=True)
    downloads= models.PositiveIntegerField(verbose_name='Nombre de Télechargement',default=0,null=True,unique=False)
    class Meta:
        verbose_name='#2-Cours'
        verbose_name_plural='#2-Cours'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file:
            if not self.hash:
                self.hash= make_hash(self.file)

            if Cours.objects.filter(hash=self.hash).exclude(pk=self.pk).exists():
                raise ValidationError({'error_cour_1':"Ce PDF est déja disponinle"})


            if Document.objects.filter(hash=self.hash).exists():
                raise ValidationError({'error_cour_2':"Ce PDF est disponible en tant qu'exercie"})

            if Document.objects.filter(correction_hash=self.hash).exists():
                raise ValidationError({'error_cour_3':"Ce PDF est disponible en tant que correction"})


        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.file:
            cour_without_pdf= self.file.name.replace('.pdf','')
            name= cour_without_pdf.replace('cours/','')

            # A activez une fois les configurations terminer
            if self.file.size > 20*1024*1024:
                raise  ValidationError('Fichier volumineux (>20Mo)')
            
            if not self.name:
                self.name= name

            try:
                cours= PdfReader(self.file)
                if not cours.pages:
                    raise ValidationError('Ce pdf est vide.')
            except Exception:
                raise ValidationError('PDF non valide')
        

class Document(models.Model):

    name= models.CharField(max_length=200,verbose_name='Nom',null=True,blank=True,unique=True)
    file= models.FileField(upload_to='./Document',validators=[FileExtensionValidator(allowed_extensions=['pdf'])],verbose_name='fichier')
    correction= models.FileField(upload_to='./correction',validators=[FileExtensionValidator(allowed_extensions=['pdf'])],verbose_name='Correction',null=True,blank=True,)

    hash= models.CharField(max_length=64,unique= True,null=True,blank=True,verbose_name='hash du fichier')
    correction_hash= models.CharField(max_length=64,unique= True,null=True,blank=True,verbose_name='hash du correction',)

    filiere= models.ForeignKey(Filiere,on_delete=models.CASCADE,default="",null=True,blank=True,verbose_name='Filière',related_name='filiere')
    level= models.ForeignKey(NiveauEtude,on_delete=models.CASCADE,default="",null=True,blank=True,verbose_name='Niveau',related_name='level')
    type= models.ForeignKey(TypeOf,on_delete=models.CASCADE,null=True,blank=True,related_name='type')

    add_date= models.DateTimeField(auto_now_add=True)
    publier_par= models.ForeignKey(User,on_delete= models.CASCADE,null=True,blank=True,)
    publier= models.BooleanField(verbose_name='Publier le fichier',default=False)
    downloads= models.PositiveIntegerField(verbose_name='Nombre de Télechargement',default=0,null=True,unique=False)

    class Meta:
        verbose_name='#3-Exercie & Sujet'
        verbose_name_plural='#3-Exercices & Sujets'

    def save(self, *args, **kwargs):

        if self.file:
            if not self.hash:
                self.hash= make_hash(self.file)

        if self.correction:
            if self.pk:
                objet= Document.objects.get(pk=self.pk)
                if self.correction != objet.correction:
                        self.correction_hash= make_hash(self.correction)
            else:
                self.correction_hash= make_hash(self.correction)


            if Document.objects.filter(hash=self.correction_hash).exists():
                raise ValidationError({'error_document_5':"Nous disposons de cette correction comme Exercice ou Sujet"})

            if Cours.objects.filter(hash=self.correction_hash).exists():
                raise ValidationError({'error_document_3':"Nous disposons de votre correction comme cours"})
            

        if Document.objects.filter(hash=self.hash).exclude(pk=self.pk).exists():
            raise ValidationError({'error_document_1': 'Pdf existant'})

        if Document.objects.filter(correction_hash=self.hash).exists():
            raise ValidationError({'error_document_2':"Nous disposons de ce pdf comme correction"})

        if Cours.objects.filter(hash=self.hash).exists():
            raise ValidationError({'error_document_4':"Nous disposons de votre exercice comme cours"})


        return super().save(*args, **kwargs)


    def __str__(self):
        return self.name

 
    def clean(self):
        super().clean()

        name_wthiout_pdf= self.file.name.replace('.pdf','')
        name= name_wthiout_pdf.replace('Document/','')

        if not self.name:
            self.name=name
            self.correction_hash=f'hash_du_correction_{name[0:30]}'

        if self.file:

            # A activez une fois les configurations terminer
            if self.file.size > 20*1024*1024:
                raise  ValidationError('Fichier volumineux (>20Mo)')

            try:
                file = PdfReader(self.file)
                if not file.pages:
                    raise ValidationError("Ce PDF est vide")
            except:
                raise ValidationError("PDF non valide.")
            

        if self.correction:

            # A activez une fois les configurations terminer
            if self.correction.size > 20*1024*1024:
                raise  ValidationError('Correction volumineux (>20Mo)')

            try:
                correction= PdfReader(self.correction)
                if not correction.pages:
                    raise ValidationError("Cet correction est vide")
            except Exception:
                raise ValidationError("Correction non valide.")
        
# like et favoris traitement
class DocumentLike(models.Model):
    user= models.ForeignKey(User,on_delete= models.CASCADE,verbose_name="Utilisateur")
    document= models.ForeignKey(Document,on_delete= models.CASCADE,verbose_name='Exercice & Sujets')
    like= models.BooleanField(verbose_name='like',default=True)

    class Meta:
        verbose_name='Z-Like-Exercice & Sujets'
        verbose_name_plural='Z-Like-Exercice & Sujets'
        unique_together=('user','document')

    def __str__(self):
        return self.user.username

class CoursLike(models.Model):
    user= models.ForeignKey(User,on_delete= models.CASCADE,verbose_name="Utilisateur")
    cours= models.ForeignKey(Cours,on_delete= models.CASCADE,verbose_name='Cours')
    like= models.BooleanField(verbose_name='like',default=True)

    class Meta:
        verbose_name= 'Z-Like-Cours'
        verbose_name_plural= 'Z-Like-Cours'
        unique_together=('user','cours')

    def __str__(self):
        return self.user.username

class EventLike(models.Model):
    user= models.ForeignKey(User,on_delete= models.CASCADE,verbose_name="Utilisateur")
    event= models.ForeignKey(Events,on_delete= models.CASCADE,verbose_name='Evenements')
    like= models.BooleanField(verbose_name='like',default=True)

    class Meta:
        verbose_name='Z-Like-Évenement'
        verbose_name='Z-Like-Évenements'
        unique_together=('user','event')

    def __str__(self):
        return self.user.username

class FavorisDocument(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateurs')
    pdf= models.ForeignKey(Document, on_delete= models.CASCADE, verbose_name='Document',null=True)
    favoris= models.BooleanField(verbose_name='Favoris',default=False,unique=False,null=True)
    
    class Meta:
        verbose_name='Z-Favoris-Exercice & Sujets'
        verbose_name_plural='Z-Favoris-Exercice & Sujets'
        unique_together=('user','pdf')

    def __str__(self):
        return self.user.username

class FavorisCours(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateurs')
    pdf= models.ForeignKey(Cours, on_delete= models.CASCADE, verbose_name='Cours',null=True)
    favoris= models.BooleanField(verbose_name='Favoris',default=False,unique=False,null=True)

    class Meta:
        verbose_name='Z-Favoris-Cours'
        verbose_name_plural='Z-Favoris-Cours'
        unique_together=('user','pdf')

    def __str__(self):
        return self.user.username

# like et favoris traitement

@receiver(pre_save,sender=Profil)
def get_inst(sender,instance,*args, **kwargs):
    try:
        old_instance= Profil.objects.get(user= instance.user)
        if old_instance.image != instance.image:
            if old_instance.image:  
                old_instance.image.delete(save=True)
            if instance.image:
                try:
                    instance.image=compressor(instance.image,instance.user.username)
                except:
                    return None

    except:
        old_instance=None

@receiver(pre_save,sender=Events)
def get_inst(sender,instance,*args, **kwargs):
    try:
        if instance.pk:
            old_instance= Events.objects.get(name= instance.name)
            if old_instance.image != instance.image:
                if old_instance.image:  
                    old_instance.image.delete(save=True)
                if instance.image:
                    try:
                        instance.image=compressor(instance.image,instance.user.username)
                    except:
                        return None
        else:
            if instance.image:
                instance.image=compressor(instance.image,instance.name)

    except:
        old_instance=None


@receiver(pre_delete, sender=Document)
def check_media_document(sender,instance,*args,**kwargs):
    instance.file.delete()
    if instance.correction:
        instance.correction.delete()

@receiver(pre_delete, sender=Cours)
def check_media_cours(sender,instance,*args,**kwargs):
        instance.file.delete()


@receiver(pre_save, sender=Document)
def check_save_document(sender, instance,*args, **kwargs):
    if instance.pk:
        if instance.correction:
            old_instance= Document.objects.get(pk= instance.pk)
            if old_instance.correction_hash != instance.correction_hash:
                if old_instance.correction:
                    old_instance.correction.delete(save=True)

