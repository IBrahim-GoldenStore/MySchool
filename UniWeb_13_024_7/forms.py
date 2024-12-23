from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from UniWeb_13_024_7.models import *

class AddPDF(forms.ModelForm):
    class Meta:
        model= Document
        fields=['file','correction']


class AddCour(forms.ModelForm):
    class Meta:
        model=Cours
        fields=['file']

    
#  lier au gestion du compte 
class Avatar(forms.ModelForm):
    class Meta:
        model= Profil
        fields=['image']


class Bio(forms.ModelForm):
    university= forms.CharField(max_length=70,required=True,help_text='Établissement')
    filiere= forms.ModelChoiceField(queryset=Filiere.objects.all(),required=True,help_text="Filière")
    level= forms.ModelChoiceField(queryset=NiveauEtude.objects.all(),required=True,help_text="Niveau d'étude")
    bio= forms.CharField(max_length=255,required=True,help_text='Biographie',widget=forms.Textarea(attrs={'placeholder': 'Entrez votre nouvelle Biographie','maxlength':400,}),)
    class Meta:
        model= Profil
        fields= ['university','filiere','level','bio']

class SiginForm(UserCreationForm):
    email= forms.EmailField(label='Email')
    class Meta:
        model= User
        fields= ['username','password1','password2','email',]
        help_text={
            'username':'Nom',
        }
    
    def save(self, commit= True):
        user = super().save(commit=False)
        user.email= self.cleaned_data['email']
        if commit:
            user.save()
        return user

class Password_Email(PasswordResetForm):
    email= forms.EmailField(help_text='Email')
    class Meta:
        fields=['email']