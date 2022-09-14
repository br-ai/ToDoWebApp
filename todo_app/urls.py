from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [

    path("", views.home, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("modifier/<int:id>", views.modifier, name="modifier"),
    path("supprimer/<int:id>", views.supprimer, name="supprimer"),
    path("creer_tache", views.creer_tache, name="creer_tache"),
    path("changeState/<int:id>", views.changeState, name="changeState"),
    path("historique", views.historique, name="historique"),
    path("cloture", views.cloture, name="cloture"),


    ]
