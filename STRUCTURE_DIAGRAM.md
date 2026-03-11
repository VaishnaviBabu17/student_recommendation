# Project Structure Diagram

## 📁 Complete Directory Structure

```
student_recommendation/
│
├── 🎨 frontend/                          # All Frontend Files
│   ├── templates/                        # HTML Templates
│   │   ├── 👨‍💼 Admin Templates
│   │   │   ├── admin_dashboard.html      # Admin control panel
│   │   │   ├── admin_analytics.html      # System analytics
│   │   │   ├── admin_academic_records.html
│   │   │   └── ... (other admin pages)
│   │   │
│   │   ├── 👨‍🎓 Student Templates
│   │   │   ├── student_dashboard.html    # Student main page
│   │   │   ├── student_marks.html        # Marks entry form
│   │   │   ├── student_recommendation.html # Recommendations
│   │   │   ├── student_info.html         # Student information
│   │   │   └── base_student.html         # Base template
│   │   │
│   │   ├── 🔐 Authentication Templates
│   │   │   ├── login.html                # Login page
│   │   │   ├── register.html             # Registration page
│   │   │   └── reset_password.html       # Password reset
│   │   │
│   │   └── 🏠 General Templates
│   │       ├── home.html                 # Landing page
│   │       └── select_role.html          # Role selection
│   │
│   └── static/                           # Static Files
│       └── css/
│           └── theme.css                 # Custom styles
│
├── ⚙️ backend/                           # All Backend Files
│   ├── student_recommendation/           # Django Project Config
│   │   ├── __init__.py
│   │   ├── settings.py                   # ✅ Updated paths
│   │   ├── urls.py                       # URL routing
│   │   ├── wsgi.py                       # ✅ Updated for deployment
│   │   └── asgi.py                       # ASGI config
│   │
│   └── students/                         # Main Django App
│       ├── migrations/                   # Database migrations
│       │   ├── 0001_initial.py
│       │   ├── 0002_...py
│       │   └── __init__.py
│       │
│       ├── __init__.py
│       ├── models.py                     # Database models
│       │   ├── Student
│       │   ├── AcademicRecord
│       │   └── InternalMark
│       │
│       ├── views.py                      # Business logic
│       │   ├── Authentication views
│       │   ├── Student views
│       │   └── Admin views
│       │
│       ├── urls.py                       # App URLs
│       ├── admin.py                      # Admin configuration
│       ├── signals.py                    # Django signals
│       └── tests.py                      # Unit tests
│
├── 📄 Root Files
│   ├── manage.py                         # ✅ Updated Python path
│   ├── db.sqlite3                        # Database file
│   ├── requirements.txt                  # Python dependencies
│   ├── .gitignore                        # Git ignore rules
│   ├── .env.example                      # Environment variables template
│   │
│   ├── 📚 Documentation
│   │   ├── README.md                     # Main documentation
│   │   ├── PROJECT_STRUCTURE.md          # Structure guide
│   │   ├── REORGANIZATION_GUIDE.md       # Quick start
│   │   ├── REORGANIZATION_SUMMARY.md     # Changes summary
│   │   └── STRUCTURE_DIAGRAM.md          # This file
│   │
│   └── 🚀 Deployment Files
│       ├── Procfile.txt                  # Heroku/Render config
│       ├── RENDER_DEPLOYMENT.md          # Deployment guide
│       └── RUN_MIGRATIONS.txt            # Migration instructions
│
└── 🔧 Configuration
    └── .github/
        └── workflows/
            └── django.yml                # CI/CD configuration
```

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        USER REQUEST                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         manage.py                            │
│                  (adds backend/ to path)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              backend/student_recommendation/                 │
│                       urls.py                                │
│                  (routes to views)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  backend/students/                           │
│                     views.py                                 │
│              (processes business logic)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  backend/students/                           │
│                    models.py                                 │
│              (database operations)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    frontend/templates/                       │
│                  (renders HTML)                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    frontend/static/                          │
│                  (loads CSS/JS)                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      USER RESPONSE                           │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Key Relationships

### Settings Configuration
```
backend/student_recommendation/settings.py
    │
    ├──> TEMPLATES['DIRS'] ──────> frontend/templates/
    ├──> STATICFILES_DIRS ───────> frontend/static/
    ├──> DATABASES ──────────────> db.sqlite3 (root)
    └──> INSTALLED_APPS ─────────> backend/students/
```

### URL Routing
```
backend/student_recommendation/urls.py
    │
    └──> include('students.urls') ──> backend/students/urls.py
            │
            ├──> /login/ ──────────────> views.login_view()
            ├──> /register/ ───────────> views.register_student()
            ├──> /student/dashboard/ ──> views.student_dashboard()
            ├──> /student/marks/ ──────> views.student_marks()
            └──> /admin/dashboard/ ────> views.admin_dashboard()
```

## 📊 Component Interaction

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Frontend   │◄────────│   Backend    │◄────────│   Database   │
│  Templates   │         │    Views     │         │   Models     │
└──────────────┘         └──────────────┘         └──────────────┘
       │                        │                         │
       │                        │                         │
       ▼                        ▼                         ▼
  HTML/CSS/JS            Python Logic              SQLite DB
  User Interface         Business Rules            Data Storage
```

## ✅ Updated Files Summary

| File | Location | Changes |
|------|----------|---------|
| settings.py | backend/student_recommendation/ | ✅ Paths updated |
| manage.py | root | ✅ Python path added |
| wsgi.py | backend/student_recommendation/ | ✅ Python path added |
| templates/ | frontend/templates/ | ✅ Moved location |
| static/ | frontend/static/ | ✅ Moved location |
| students/ | backend/students/ | ✅ Moved location |
| student_recommendation/ | backend/student_recommendation/ | ✅ Moved location |

## 🎨 Frontend Structure Detail

```
frontend/
├── templates/
│   ├── Admin Pages (7 files)
│   ├── Student Pages (5 files)
│   ├── Auth Pages (3 files)
│   └── General Pages (2 files)
│
└── static/
    └── css/
        └── theme.css (Professional green theme)
```

## ⚙️ Backend Structure Detail

```
backend/
├── student_recommendation/
│   ├── Configuration files (5 files)
│   └── Project settings
│
└── students/
    ├── Core logic (7 files)
    ├── Database models
    ├── View functions
    └── URL routing
```

---

**This structure provides clear separation while maintaining all functionality!** 🎉