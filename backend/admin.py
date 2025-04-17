from django.contrib import admin
from .models import Category, Author, Book, BookAuthor


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name',)


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1  # Show 1 empty row to add new relationships

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    inlines = [BookAuthorInline]

    list_display = ('title', 'category', 'publication_date', 'copies_owned')

    search_fields = ('title',)

    list_filter = ('category', 'publication_date')