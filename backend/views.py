from django.shortcuts import render

from backend.models import Category, AdminUser, AuthorUser, MemberUser, Book, CustomUser


# Create your views here.
def dashboard_callback(request, context):
    admins_count = CustomUser.objects.filter(groups__name='Admin').count()
    authors_count = CustomUser.objects.filter(groups__name='Author').count()
    members_count = CustomUser.objects.filter(groups__name='Member').count()
    category_count = Category.objects.count()
    books_count = Book.objects.count()

    context.update({
        "admins_count": admins_count,
        "authors_count": authors_count,
        "members_count": members_count,
        "category_count": category_count,
        "books_count": books_count
    })

    return context