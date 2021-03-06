from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('users/', list_users, name="list_users"),
    path('users/update/<int:user_id>/', update_user_status, name="update_user_status"),
    path('users/delete/<int:user_id>/', delete_user, name="delete_user"),
    path('users/download/', download_users, name="download_users"),
    path('email/', send_email, name="send_email")
]
