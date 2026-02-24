from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_student, name='register_student'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student_info/', views.student_info, name='student_info'),
    path('student_marks/', views.student_marks, name='student_marks'),
    path('student_recommendation/', views.student_recommendation, name='student_recommendation'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_add_student/', views.admin_add_student, name='admin_add_student'),
    path('admin_edit_student/<int:student_id>/', views.admin_edit_student, name='admin_edit_student'),
    path('admin_delete_student/<int:student_id>/', views.admin_delete_student, name='admin_delete_student'),
    path('admin_academic_records/', views.admin_academic_records, name='admin_academic_records'),
    path('admin_add_academic_record/', views.admin_add_academic_record, name='admin_add_academic_record'),
    path('admin_bulk_upload/', views.admin_bulk_upload, name='admin_bulk_upload'),
    path('admin_view_recommendations/<int:student_id>/', views.admin_view_recommendations, name='admin_view_recommendations'),
    path('admin_analytics/', views.admin_analytics, name='admin_analytics'),
    path('export_students_pdf/', views.export_students_pdf, name='export_students_pdf'),
    path('logout/', views.logout_view, name='logout'),
    path('create_admin/', views.create_admin, name='create_admin'),
]