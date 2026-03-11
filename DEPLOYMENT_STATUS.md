# Deployment Currently Disabled

## ⚠️ Important Notice

The deployment to Render.com is currently **disabled** due to the recent project reorganization.

## 🔧 What Changed

The project structure was reorganized into separate `frontend/` and `backend/` folders for better maintainability and professional organization. This change requires updates to the deployment configuration.

## 📋 Current Status

- ✅ **Local Development**: Working perfectly
- ✅ **GitHub Repository**: Up to date
- ⏸️ **Render Deployment**: Temporarily disabled

## 🚀 To Re-enable Deployment

### Option 1: Update Render Configuration (Recommended)

1. Go to your Render dashboard
2. Update the **Build Command**:
   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```

3. Update the **Start Command**:
   ```bash
   gunicorn --pythonpath backend student_recommendation.wsgi:application
   ```

4. Set Environment Variables:
   - `PYTHON_VERSION`: 3.11
   - `DEBUG`: False
   - `SECRET_KEY`: (generate a secure key)
   - `ALLOWED_HOSTS`: .onrender.com

### Option 2: Use render.yaml (Automatic)

The `render.yaml` file in the root directory contains all necessary configuration. Render should automatically detect and use it.

### Option 3: Manual Deployment Setup

If automatic detection fails:

1. **Root Directory**: Keep as project root
2. **Build Command**: 
   ```bash
   pip install -r requirements.txt && python manage.py migrate
   ```
3. **Start Command**: 
   ```bash
   gunicorn --pythonpath backend student_recommendation.wsgi:application --bind 0.0.0.0:$PORT
   ```

## 📝 Notes

- The database file (`db.sqlite3`) is in the root directory
- Templates are in `frontend/templates/`
- Static files are in `frontend/static/`
- Django settings are in `backend/student_recommendation/settings.py`
- All paths have been updated in the code

## ✅ Local Development Works

To run locally:
```bash
python manage.py runserver
```

Everything works perfectly in local development. The deployment configuration just needs to be updated on Render's side.

## 🔄 Future Deployment

Once the Render configuration is updated, deployment will work normally. All functionality is preserved - only the folder structure changed.

---

**Last Updated**: March 11, 2026  
**Status**: Deployment configuration pending update