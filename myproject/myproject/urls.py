from django.contrib import admin
from django.urls import path
from main import views as main_views


urlpatterns = [
    path('', main_views.index, name="index"),
    path('depression/', main_views.depression),
    path('chatbot/', main_views.chatbot),
    path('admin/', admin.site.urls)
]