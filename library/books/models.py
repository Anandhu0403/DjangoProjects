from django.db import models

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=20)
    author=models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    pages=models.IntegerField()
    price=models.IntegerField()
    cover=models.ImageField(upload_to="images")
    pdf=models.FileField(upload_to="pdf")