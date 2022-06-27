from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    
    path('login',views.login),
    path('logout',views.logout),
    path('books',views.books),
    path('books/<int:bookId>',views.view),
    path('delete',views.delete),
    path('books/<int:bookId>/favorite',views.favorite),
    path('books/<int:book_id>/unfavorite', views.unfavorite)
]