from django.shortcuts import render
from .models import Student

# SUBJECTS FOR EACH DEPARTMENT & SEMESTER
SUBJECTS = {

    "ECE": {
        1: ["Mathematics 1", "Physics", "Basic Electrical"],
        3: ["Signals and Systems", "Analog Electronics"],
        5: ["Digital Communication", "DSP", "Transmission Lines", "IoT"]
    },

    "CSE": {
        1: ["Mathematics 1", "Programming in C"],
        3: ["Data Structures", "OOP"],
        5: ["Operating Systems", "Computer Networks", "DBMS"]
    },

    "EEE": {
        1: ["Mathematics", "Physics"],
        5: ["Power Systems", "Control Systems"]
    },

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


# BOOKS AND LEARNING RESOURCES
RESOURCES = {

    "Digital Communication": [
        "Simon Haykin Book",
        "NPTEL Digital Communication"
    ],

    "DSP": [
        "Oppenheim DSP",
        "NPTEL DSP Course"
    ],

    "Operating Systems": [
        "Galvin OS Book",
        "MIT OCW"
    ],

    "Digital Communication": [
        "Digital Communication by Simon Haykin",
        "NPTEL Digital Communication Course"
    ],

    "Digital Signal Processing": [
        "DSP by Oppenheim",
        "NPTEL DSP Course"
    ],

    "Transmission Lines and Antennas": [
        "Antenna Theory by Balanis",
        "NPTEL Antenna Course"
    ],

    "IoT and Applications": [
        "Internet of Things by Arshdeep Bahga",
        "Coursera IoT Specialization"
    ],

    "Operating Systems": [
        "Operating System Concepts by Galvin",
        "MIT OpenCourseWare"
    ]
}

def get_subjects(department, semester):
    return SUBJECTS.get(department, {}).get(semester, [])


def home(request):

    subjects = []
    recommendations = {}

    if request.method == "POST":

        reg_no = request.POST['reg_no']
        name = request.POST['name']
        department = request.POST['department']
        year = int(request.POST['year'])
        semester = int(request.POST['semester'])

        subjects = get_subjects(department, semester)

        # SAVE STUDENT BASIC DETAILS
        Student.objects.create(
            reg_no=reg_no,
            name=name,
            department=department,
            year=year,
            semester=semester
        )

        # LOOP FOR EACH SUBJECT
        for sub in subjects:

            marks = int(request.POST.get(sub + "_marks") or 0)
            attended = int(request.POST.get(sub + "_attended") or 0)
            total = int(request.POST.get(sub + "_total") or 1)

            attendance_percentage = (attended / total) * 100 if total > 0 else 0

            rec = []

            # MARKS BASED RECOMMENDATION
            if marks < 50:
                rec.append("Marks are low. Improve preparation.")

            # ATTENDANCE BASED RECOMMENDATION
            if attendance_percentage < 75:
                rec.append("Attendance below 75%. Attend classes regularly.")

            # ADD STUDY RESOURCES
            rec.extend(RESOURCES.get(sub, []))

            recommendations[sub] = {
                "marks": marks,
                "attendance": round(attendance_percentage, 2),
                "recommendations": rec
            }

    return render(request, "home.html", {
        "subjects": subjects,
        "recommendations": recommendations
    })


from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin123'
        )
        return HttpResponse("Superuser created successfully")

    return HttpResponse("Admin already exists")
