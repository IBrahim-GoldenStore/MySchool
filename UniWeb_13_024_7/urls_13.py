from django.urls import path
from UniWeb_13_024_7 import views

app_name = "main"

urlpatterns = [
    path('', views.index_view, name='index'),
    path('cours', views.cours_view, name='cours'),
    path('exercices', views.exo_view, name='exo'),
    path('sigin', views.sigin_views, name='sigin'),
    path('login', views.login_views, name='login'),
    path('logout', views.logout_views, name='logout'),
    path('compte',views.compte_view, name='compte'),
    path('Actualités',views.events_view,name='events'),
    path('Actualités/<str:event_name>',views.event_details,name='event_detail'),
    path('exercices/filtre/<str:name>',views.filter_view_exo,name='filtre'),
    path('cours/filtre/<str:name>',views.filter_view_cours,name='filtre_cours'),
    path('pdf_info/<str:name>',views.single_pdf_view, name='pdf'),
    path('remove/avatar/<str:username>',views.remove_view, name='remove'),
    path('update/<str:username>',views.update_view, name='update'),
    path('delete/<str:username>',views.delete_view, name='delete'),
    path('password',views.SendChangepassword_view, name='passwordEmail'),
    path('newpassword/<uid64>/<token>',views.newPassword_view,name='newpassword'),
    path('download/<str:objet_type>/<int:objet_id>',views.download,name='download'),
    path('like_pdf/<str:pdf_name>/<int:user_id>/<str:etat>',views.like_document,name='like'),
    path('like_event/<int:event_id>/<int:user_id>/<str:etat>',views.like_event,name='like_event'),
    path('favoris/<str:pdf_name>/<int:user_id>/<str:etat>',views.FavorisGestion,name='favoris'),
    path('read/<str:pdf_name>',views.read_view,name='read'),
    # path('pagination/',views.paginator_view_for_document,name='pagination'),
    # path('paginations/',views.paginator_view_for_cours,name='cours_pagination'),
    # redirection
    path('redirect_of_exo/<str:lien>',views.exo_redirect,name='exo_redirect'),
    path('redirect_of_sujet',views.sujet_redirect,name='sujet_redirect'),
    path('redirect_of_delete1',views.success_delete,name='success_delete'),
    path('redirect_of_email',views.email_redirect,name='email_redirect'),
    path('download_error',views.download_error,name='download_redirect'),
    path('error/<str:message>/<str:lien>', views.error_view,name='error'),

]