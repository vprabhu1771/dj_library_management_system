from django.urls import path

from frontend.views import home, member_register, member_login, member_logout, member_dashboard, books_list, \
    loaned_books, fines_view, pay_fine, payment_success, reservations_view

urlpatterns = [
    path('', home),

    path('books_list/', books_list, name='books_list'),

    path('', member_dashboard, name='member_dashboard'),

    path('register/', member_register, name='register'),

    path('login/', member_login, name='login'),

    path('logout/', member_logout, name='logout'),

    path('loans/', loaned_books, name='loaned_books'),

    path('fines/', fines_view, name='fines'),

    path('fines/pay/<int:fine_id>/', pay_fine, name='pay_fine'),

    path('fines/payment-success/', payment_success, name='payment_success'),

    path('reservations/', reservations_view, name='reservations'),
]