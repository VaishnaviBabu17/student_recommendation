from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'roll_no', 'department', 'year', 'semester']
    
    def save_model(self, request, obj, form, change):
        if not obj.roll_no and obj.user:
            obj.roll_no = obj.user.username
        super().save_model(request, obj, form, change)