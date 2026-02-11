from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    semester = models.IntegerField()

    total_classes = models.IntegerField()
    classes_attended = models.IntegerField()

    def attendance_percentage(self):
        if self.total_classes == 0:
            return 0
        return (self.classes_attended / self.total_classes) * 100
