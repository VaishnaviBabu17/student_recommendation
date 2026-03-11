from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, blank=True, null=True)
    roll_no = models.CharField(max_length=50, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academic_records')
    subject = models.CharField(max_length=200)
    internal_type = models.CharField(max_length=20)  # Internal 1 or Internal 2
    marks = models.IntegerField()  # Out of 50
    attendance_attended = models.IntegerField(default=0)
    attendance_total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'subject', 'internal_type']

    def __str__(self):
        return f"{self.student.user.username} - {self.subject} - {self.internal_type}"

    @property
    def attendance_percentage(self):
        if self.attendance_total > 0:
            return round((self.attendance_attended / self.attendance_total) * 100, 2)
        return 0