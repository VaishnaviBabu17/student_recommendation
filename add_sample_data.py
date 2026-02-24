import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_recommendation.settings')
django.setup()

from students.models import Student, AcademicRecord

# Get existing students
students = Student.objects.filter(department__isnull=False)

if students.count() == 0:
    print("No students with complete profiles found!")
    print("Please add students with department and semester information first.")
else:
    for student in students:
        print(f"\nAdding records for {student.name} ({student.department})")
        
        # Get subjects based on department and semester
        from students.views import SUBJECTS
        subjects = SUBJECTS.get(student.department, {}).get(student.semester, [])
        
        if not subjects:
            print(f"  ⚠️ No subjects found for {student.department} Semester {student.semester}")
            continue
        
        # Add marks for Internal 1
        for i, subject in enumerate(subjects):
            marks = [45, 38, 22, 35, 42][i % 5]  # Mix of weak, average, strong
            AcademicRecord.objects.update_or_create(
                student=student,
                subject=subject,
                internal_type="Internal 1",
                defaults={
                    'marks': marks,
                    'attendance_attended': 40 + i*2,
                    'attendance_total': 50
                }
            )
            print(f"  - {subject}: {marks}/50")

print("\nSample data added successfully!")
print("Now login as admin and check Academic Records, Analytics, and View Report")
