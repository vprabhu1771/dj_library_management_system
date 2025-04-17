from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"


class Author(models.Model):
    id = models.BigAutoField(primary_key=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "author"

class Book(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=255)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    publication_date = models.DateField()

    copies_owned = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "book"