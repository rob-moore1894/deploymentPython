from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('quotes', views.quotesPage),
    path('addQuote', views.addQuote),
    path('user/<int:uploaderId>', views.userPage),
    path('like/<int:quoteId>', views.addLike),
    path('myaccount/<int:userId>', views.editPage),
    path('update', views.updateUser),
    path('logout', views.logout),
]