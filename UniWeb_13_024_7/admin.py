from django.contrib import admin
from UniWeb_13_024_7.models import *
from django.contrib import messages

@admin.register(Profil)
class AdminProfil(admin.ModelAdmin):
    list_display=['user','status','university','filiere','level','image','bio']

@admin.register(Document)
class AdminDocument(admin.ModelAdmin):
    list_display=['name','type','correction','filiere','level','publier']
    readonly_fields=('file','hash','add_date','publier_par','correction_hash','downloads')

@admin.register(Filiere)
class AdminFilier(admin.ModelAdmin):
    list_display=['sigle','name']

@admin.register(NiveauEtude)
class AdminNiveauEtude(admin.ModelAdmin):
    list_display=['name']

@admin.register(TypeOf)
class AdminTypeOf(admin.ModelAdmin):
    list_display=['name']

@admin.register(Cours)
class AdminCours(admin.ModelAdmin):
    list_display=['name','filiere','level','matiere']
    readonly_fields=['file','publier_par','hash','add_date','downloads']

@admin.register(Events)
class AdminEvents(admin.ModelAdmin):
    list_display=['name','apercu_rapide','description','image','file']
    readonly_fields=['add_date']

@admin.register(DocumentLike)
class AdminDocumentLike(admin.ModelAdmin):
    readonly_fields=['user','document','like']

@admin.register(CoursLike)
class AdminCoursLike(admin.ModelAdmin):
    readonly_fields=['user','cours','like']


@admin.register(EventLike)
class AdminEventLike(admin.ModelAdmin):
    readonly_fields=['user','event','like']

@admin.register(FavorisCours)
class AdminFavorisCour(admin.ModelAdmin):
    readonly_fields=['user','pdf','favoris']

@admin.register(FavorisDocument)
class AdminFavorisDocument(admin.ModelAdmin):
    readonly_fields=['user','pdf','favoris']