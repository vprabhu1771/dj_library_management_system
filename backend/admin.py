from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from backend.forms import CustomUserCreationForm, CustomUserChangeForm
from backend.models import CustomUser
from django.utils.html import format_html

from .models import Category, Author, Book, BookAuthor


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    form = CustomUserChangeForm

    model = CustomUser

    list_display = ('email', 'gender', 'image_tag', 'is_staff', 'is_active',)

    list_filter = ('email', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'gender', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'gender', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    search_fields = ('email',)

    ordering = ('email',)

    def image_tag(self, obj):
        return format_html('<img src ="{}" width ="150" height="150" />'.format(obj.image.url))

    image_tag.short_description = 'Image'

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