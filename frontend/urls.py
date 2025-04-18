from django.urls import path

from frontend.views import home, member_register, member_login

urlpatterns = [
    path('', home),

    path('register/', member_register, name='register'),

    path('login/', member_login, name='login'),
]