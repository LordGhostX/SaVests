from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('users/', list_users, name="list_users")
]
