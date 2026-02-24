# Render Deployment Instructions

## Environment Variables to Set on Render

Go to your Render dashboard → Your Web Service → Environment → Add the following:

```
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
ALLOWED_HOSTS=your-app-name.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
PYTHON_VERSION=3.11.0
```

## Generate Secret Key

Run this in Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Important Notes

1. Replace `your-app-name.onrender.com` with your actual Render URL
2. Make sure to include `https://` in CSRF_TRUSTED_ORIGINS
3. Set DEBUG=False for production
4. After setting environment variables, redeploy your app on Render
