from django.urls import path
from . import views
urlpatterns = [
#path('', views.index, name='index'),
  path('', views.affiche, name='affiche'),
    path('filtrer_par_prix/', views.filtrer_par_prix, name='filtrer_par_prix'),
    path('filtrer_par_marque/', views.filtrer_par_marque, name='filtrer_par_marque'),
    path('details/', views.details, name='details'),
]