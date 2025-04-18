from django.urls import path

from frontend.views import home, member_register, member_login, member_logout

urlpatterns = [
    path('', home),

    path('register/', member_register, name='register'),

    path('login/', member_login, name='login'),

    path('logout/', member_logout, name='logout'),
]