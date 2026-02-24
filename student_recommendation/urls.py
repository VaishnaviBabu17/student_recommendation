from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # connect app urls
    path('', include('students.urls')),
    
]
