from django.contrib import admin
from .models import Category, Author, Book


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('title', 'category', 'publication_date', 'copies_owned')

    search_fields = ('title',)

    list_filter = ('category', 'publication_date')