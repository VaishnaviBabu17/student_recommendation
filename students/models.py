from django.db import models

class Student(models.Model):
    reg_no = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    year = models.IntegerField()
    semester = models.IntegerField()
