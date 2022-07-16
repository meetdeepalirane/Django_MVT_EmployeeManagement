from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.contrib.auth.decorators import login_required

from .views import success, employee_image_view

urlpatterns = [
    path("", views.index, name="index"),
    path("all_emp", views.all_emp, name="all_emp"),
    path("add_emp", views.add_emp, name="add_emp"),
    path("delete_emp", views.delete_emp, name="delete_emp"),
    path("delete_emp/<int:emp_id>", views.delete_emp, name="delete_emp"),
    path("filter_emp", views.filter_emp, name="filter_emp"),
    path("update_emp/<int:emp_id>", views.update_emp, name="update_emp"),
    path('feedback/', views.feedback, name='feedback'),
    path('logout', views.logout_view, name="logout"),
    path('image_upload/', views.employee_image_view, name='image_upload'),
    path('success', success, name='success'),
    path('gallery/<int:emp_id>', views.gallery, name='gallery'),
    path('register/', views.register, name='register'),
    path('statistics/',views.statistics,name='statistics')


]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
