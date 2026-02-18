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

    if request.method == "POST":

        action = request.POST.get("action")

        # ---------- LOAD SUBJECTS ----------
        if action == "load_subjects":

            reg_no = request.POST.get("reg_no")
            name = request.POST.get("name")
            department = request.POST.get("department")
            year = int(request.POST.get("year", 0))
            semester = int(request.POST.get("semester", 0))

            subjects = get_subjects(department, semester)

            Student.objects.create(
                reg_no=reg_no,
                name=name,
                department=department,
                year=year,
                semester=semester
            )

            return render(request, "home.html", {
                "subjects": subjects
            })

        # ---------- GET RECOMMENDATION ----------
        elif action == "get_recommendation":

            subjects = request.POST.getlist("subjects")

            total_marks_sum = 0
            total_attendance_sum = 0
            weak_subjects = []
            strong_subjects = []

            subject_names = []
            marks_data = []
            attendance_data = []

            for sub in subjects:

                marks = int(request.POST.get(sub + "_marks", 0))
                attended = int(request.POST.get(sub + "_attended", 0))
                total = int(request.POST.get(sub + "_total", 1))

                attendance_percentage = (
                    (attended / total) * 100 if total > 0 else 0
                )

                total_marks_sum += marks
                total_attendance_sum += attendance_percentage

                subject_names.append(sub)
                marks_data.append(marks)
                attendance_data.append(round(attendance_percentage, 2))

                # PERFORMANCE
                if marks >= 85:
                    performance = "Excellent"
                elif marks >= 70:
                    performance = "Good"
                elif marks >= 50:
                    performance = "Average"
                else:
                    performance = "Poor"

                if performance == "Poor":
                    weak_subjects.append(sub)

                if performance == "Excellent":
                    strong_subjects.append(sub)

                resource_data = RESOURCES.get(sub, {})

                books = resource_data.get("books", [])
                courses = resource_data.get("courses", [])
                practice = resource_data.get("practice", [])

                improvement_plan = []

                if performance == "Poor":
                    improvement_plan.append("Revise fundamentals daily.")
                    improvement_plan.append("Solve basic problems regularly.")

                elif performance == "Average":
                    improvement_plan.append("Focus on weak topics.")
                    improvement_plan.append("Increase practice sessions.")

                elif performance == "Good":
                    improvement_plan.append("Practice advanced problems.")
                    improvement_plan.append("Work on mini projects.")

                else:
                    improvement_plan.append("Explore advanced applications.")
                    improvement_plan.append("Start research or projects.")

                if attendance_percentage < 75:
                    improvement_plan.append("Improve attendance above 75%.")

                recommendations.append({
                    "subject": sub,
                    "marks": marks,
                    "attendance": round(attendance_percentage, 2),
                    "performance": performance,
                    "books": books,
                    "courses": courses,
                    "practice": practice,
                    "improvement_plan": improvement_plan
                })

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
                "recommendations": recommendations,
                "overall_marks": round(overall_marks, 2),
                "overall_attendance": round(overall_attendance, 2),
                "overall_performance": overall_performance,
                "weak_subjects": weak_subjects,
                "strong_subjects": strong_subjects,
                "subject_names": subject_names,
                "marks_data": marks_data,
                "attendance_data": attendance_data
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
