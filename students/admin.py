from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'name', 'department', 'year', 'semester')

admin.site.register(Student, StudentAdmin)
