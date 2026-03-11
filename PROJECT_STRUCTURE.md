# Student Academic Recommendation System

A comprehensive Django-based web application that provides personalized academic recommendations to students based on their performance and attendance.

## 📁 Project Structure

```
student_recommendation/
├── frontend/                    # All frontend files
│   ├── templates/              # HTML templates
│   │   ├── admin_dashboard.html
│   │   ├── student_dashboard.html
│   │   ├── student_marks.html
│   │   ├── student_recommendation.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── ... (other templates)
│   └── static/                 # CSS, JavaScript, images
│       └── css/
│           └── theme.css
│
├── backend/                     # All backend files
│   ├── student_recommendation/ # Django project settings
│   │   ├── settings.py         # Updated paths to frontend/backend
│   │   ├── urls.py
│   │   ├── wsgi.py             # Updated Python path
│   │   └── asgi.py
│   └── students/               # Main Django app
│       ├── models.py           # Database models
│       ├── views.py            # Business logic
│       ├── urls.py             # URL routing
│       ├── admin.py
│       └── migrations/
│
├── manage.py                    # Updated to use backend folder
├── db.sqlite3                   # Database file
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd student_recommendation
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```
   Or visit: `http://localhost:8000/create-admin/`

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: `http://localhost:8000/`
   - Admin panel: `http://localhost:8000/admin/`

## 🎨 Features

### For Students
- **Registration & Login** - Secure authentication system
- **Academic Profile** - Enter department, year, semester information
- **Marks Entry** - Submit marks and attendance for each subject
- **Personalized Recommendations** - Get tailored study resources based on performance
- **Performance Analytics** - View strong and weak subjects
- **Resource Library** - Access recommended books, courses, and practice materials

### For Administrators
- **Student Management** - View all registered students
- **Department Grouping** - Students organized by departments
- **Online Status Tracking** - See who's currently active
- **Search & Filter** - Find students quickly
- **Statistics Dashboard** - View system-wide metrics

## 🎯 Key Technologies

### Frontend
- HTML5
- CSS3 (Modern features: Grid, Flexbox, Gradients)
- JavaScript (Vanilla JS for interactivity)
- Django Template Language

### Backend
- Django 4.x
- Python 3.x
- SQLite (Development)
- Django ORM
- Django Authentication

## 🎨 Design Theme

Professional green color scheme:
- Primary Dark: `#1e3a1a`
- Primary: `#2d5a27`
- Primary Light: `#4a7c59`
- Accent: `#27ae60`
- Background: `#e8f5e8`, `#f8fffe`

## 📊 Supported Departments

20+ Engineering departments including:
- Computer Science (CSE, IT, ISE)
- AI/ML and Data Science (AIDS, AIML)
- Electronics (ECE, EEE, EIE)
- Mechanical (MECH, MECT)
- Civil Engineering
- Biotechnology
- And more...

## 🔧 Configuration

### Settings Updated for New Structure

The following files have been updated to work with the new folder structure:

1. **backend/student_recommendation/settings.py**
   - `TEMPLATES['DIRS']` → Points to `frontend/templates/`
   - `STATICFILES_DIRS` → Points to `frontend/static/`
   - `DATABASES` → Points to root `db.sqlite3`

2. **manage.py**
   - Added `backend/` to Python path

3. **backend/student_recommendation/wsgi.py**
   - Added `backend/` to Python path for deployment

## 📝 Usage

### Student Workflow
1. Register an account
2. Login with credentials
3. Enter academic information (department, year, semester)
4. Submit marks and attendance for subjects
5. View personalized recommendations

### Admin Workflow
1. Login with admin credentials
2. View student statistics
3. Filter students by department, online status, or alphabetically
4. Search for specific students
5. Monitor system usage

## 🔐 Default Admin Credentials

If you use the `/create-admin/` endpoint:
- Username: `admin`
- Password: `admin123`

**⚠️ Change these credentials in production!**

## 📦 Dependencies

Key packages:
- Django 4.x
- dj-database-url
- whitenoise (for static files)
- gunicorn (for production)

See `requirements.txt` for complete list.

## 🚀 Deployment

The application is configured for deployment on platforms like:
- Render
- Heroku
- PythonAnywhere
- AWS

Environment variables needed:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL` (optional)

## 📄 License

This project is for educational purposes.

## 👥 Contributors

Academic Recommendation System Team

## 📞 Support

For issues or questions, please create an issue in the repository.

---

**Note**: All functionality remains the same after reorganization. The folder structure has been updated for better organization and maintainability.