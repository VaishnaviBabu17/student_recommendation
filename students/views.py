from django.shortcuts import render
from .models import Student
from django.http import HttpResponse
from django.contrib.auth.models import User


# ================= SUBJECTS =================

SUBJECTS = {

    "ECE": {
        5: [
            "Digital Communication",
            "Digital Signal Processing",
            "Transmission Lines and Antennas",
            "IoT and Applications"
        ]
    },

    "CSE": {
        5: [
            "Operating Systems",
            "Computer Networks",
            "Artificial Intelligence",
            "Database Management Systems"
        ]
    },

    "EEE": {
        5: [
            "Power Systems",
            "Control Systems",
            "Electrical Machines"
        ]
    }
}


# ================= RESOURCES =================

RESOURCES = {

    "Digital Communication": {
        "books": [
            "Digital Communication by Simon Haykin",
            "Principles of Communication by Taub & Schilling"
        ],
        "courses": [
            "NPTEL Digital Communication",
            "MIT OCW Communication Systems"
        ],
        "practice": [
            "Previous Year University Question Papers",
            "GATE EC Practice Questions"
        ]
    },

    "Digital Signal Processing": {
        "books": [
            "DSP by Oppenheim",
            "Proakis Digital Signal Processing"
        ],
        "courses": [
            "NPTEL DSP Course",
            "Coursera DSP Specialization"
        ],
        "practice": [
            "MATLAB DSP Simulations",
            "GATE DSP Questions"
        ]
    },

    "Operating Systems": {
        "books": [
            "Operating System Concepts by Galvin",
            "Modern Operating Systems by Tanenbaum"
        ],
        "courses": [
            "MIT OpenCourseWare OS",
            "NPTEL Operating Systems"
        ],
        "practice": [
            "OS Case Study Problems",
            "GATE OS Questions"
        ]
    }
}


# ================= HELPER FUNCTION =================

def get_subjects(department, semester):
    return SUBJECTS.get(department, {}).get(semester, [])


# ================= HOME VIEW =================

def home(request):

    subjects = []
    recommendations = []

    # -------- STEP 1 : LOAD SUBJECTS --------
    if request.method == "POST" and "semester" in request.POST:

        reg_no = request.POST.get("reg_no")
        name = request.POST.get("name")
        department = request.POST.get("department")
        year = int(request.POST.get("year", 0))
        semester = int(request.POST.get("semester", 0))

        subjects = get_subjects(department, semester)

        # Save student details once
        Student.objects.create(
            reg_no=reg_no,
            name=name,
            department=department,
            year=year,
            semester=semester
        )

        return render(request, "home.html", {
            "subjects": subjects,
            "reg_no": reg_no,
            "name": name,
            "department": department,
            "year": year,
            "semester": semester
        })

    # -------- STEP 2 : GET RECOMMENDATION --------
    elif request.method == "POST":

        subjects = request.POST.getlist("subjects")

        total_marks_sum = 0
        total_attendance_sum = 0
        weak_subjects = []
        strong_subjects = []

        for sub in subjects:

            marks = int(request.POST.get(sub + "_marks", 0))
            attended = int(request.POST.get(sub + "_attended", 0))
            total = int(request.POST.get(sub + "_total", 1))

            attendance_percentage = (
                (attended / total) * 100 if total > 0 else 0
            )

            total_marks_sum += marks
            total_attendance_sum += attendance_percentage

            if marks < 50:
                weak_subjects.append(sub)

            if marks >= 80:
                strong_subjects.append(sub)

            # PERFORMANCE LEVEL
            if marks >= 85:
                performance = "Excellent"
            elif marks >= 70:
                performance = "Good"
            elif marks >= 50:
                performance = "Average"
            else:
                performance = "Poor"

            rec = []

            if marks < 50:
                rec.append("Marks are low. Focus on fundamentals and revision.")

            if attendance_percentage < 75:
                rec.append("Attendance below 75%. Attend classes regularly.")

            resource_data = RESOURCES.get(sub, {})

            if performance == "Poor":
                rec.append("Recommended Books:")
                rec.extend(resource_data.get("books", []))

                rec.append("Practice Resources:")
                rec.extend(resource_data.get("practice", []))

            elif performance == "Average":
                rec.append("Practice and Improve Using:")
                rec.extend(resource_data.get("practice", []))

            else:
                rec.append("Advanced Learning Resources:")
                rec.extend(resource_data.get("courses", []))

            recommendations.append({
                "subject": sub,
                "marks": marks,
                "attendance": round(attendance_percentage, 2),
                "performance": performance,
                "recommendations": rec
            })

        # ===== OVERALL CALCULATION =====
        total_subjects = len(subjects)

        overall_marks = total_marks_sum / total_subjects if total_subjects else 0
        overall_attendance = total_attendance_sum / total_subjects if total_subjects else 0

        if overall_marks >= 85:
            overall_performance = "Excellent"
        elif overall_marks >= 70:
            overall_performance = "Good"
        elif overall_marks >= 50:
            overall_performance = "Average"
        else:
            overall_performance = "Poor"

        return render(request, "home.html", {
            "subjects": subjects,
            "recommendations": recommendations,
            "overall_marks": round(overall_marks, 2),
            "overall_attendance": round(overall_attendance, 2),
            "overall_performance": overall_performance,
            "weak_subjects": weak_subjects,
            "strong_subjects": strong_subjects
        })

    return render(request, "home.html")


# ================= CREATE ADMIN =================

def create_admin(request):

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="admin123"
        )
        return HttpResponse("Superuser created successfully")

    return HttpResponse("Admin already exists")
