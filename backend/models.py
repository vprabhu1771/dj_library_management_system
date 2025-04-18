from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from backend.manager import CustomerUserManager

# Create your models here.

class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')

class GenderedImageField(models.ImageField):

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if not value or not hasattr(model_instance, self.attname):
            # If no image provided or new instance
            # default gender
            gender = model_instance.gender if hasattr(model_instance, 'gender') else Gender.MALE
            if gender == Gender.MALE:
                value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                value = 'profile/female_avatar.png'
            else:
                # fallback default image
                value = 'profile/default_image.jpg'

        elif model_instance.gender != getattr(model_instance, f"{self.attname}_gender_cache", None):
            # If gender has changed
            gender = model_instance.gender
            if gender == Gender.MALE:
                value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                value = 'profile/female_avatar.png'
            else:
                # fallback default image
                value = 'profile/default_image.jpg'
        setattr(model_instance, f"{self.attname}_gender_cache", model_instance.gender)
        return value

class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(_('email address'),unique=True)
    gender = models.CharField(max_length=1,choices=Gender.choices,default=Gender.MALE)
    image = GenderedImageField(upload_to='profile/',blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']
    objects = CustomerUserManager()

    def __str__(self):
        return self.email

class AuthorUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class MemberUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Member'
        verbose_name_plural = 'Members'


class AdminUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"

class Book(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=255)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    publication_date = models.DateField()

    copies_owned = models.IntegerField()

    authors = models.ManyToManyField('CustomUser', through='BookAuthor')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "book"

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_author'
        unique_together = ('book', 'author')  # prevents duplicate author entries for a book

    def __str__(self):
        return f"{self.author} - {self.book}"


class Loan(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loan_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.email} - {self.book.title}"

    class Meta:
        db_table = 'loan'

class Fine(models.Model):
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    fine_date = models.DateField()
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.member.email} - ₹{self.fine_amount} on {self.fine_date}"