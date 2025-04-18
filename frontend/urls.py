from django.urls import path

from frontend.views import home, member_register, member_login, member_logout, member_dashboard, books_list

urlpatterns = [
    path('', home),

    path('books_list/', books_list, name='books_list'),

    path('', member_dashboard, name='member_dashboard'),

    path('register/', member_register, name='register'),

    path('login/', member_login, name='login'),

    path('logout/', member_logout, name='logout'),
]