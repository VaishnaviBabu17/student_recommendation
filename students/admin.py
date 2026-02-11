from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'semester',
                    'total_classes', 'classes_attended',
                    'get_attendance')

    def get_attendance(self, obj):
        return f"{obj.attendance_percentage():.2f}%"

    get_attendance.short_description = "Attendance %"

admin.site.register(Student, StudentAdmin)
