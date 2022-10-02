from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    # Главная страница
    path('', views.index),
    # Список мороженого
    # Подробная информация о мороженом. Ждем пременную типа int,
    # и будем использовать ее под именем pk
]
