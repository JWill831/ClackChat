from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('message', views.message),
    path('admin', views.admin),
    path('delete/<int:id>', views.delete),
    path('login_admin', views.login_admin),
    path('videos',views.videos),
    path('articles', views.articles),
    path('vendors', views.vendors),
    path('qmk', views.qmk),
    path('games',views.games),
    
]
