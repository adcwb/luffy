from django.urls import path, re_path
from . import views


urlpatterns = [
    path(r'categorys/', views.CategoryView.as_view(), ),
    path(r'courses/', views.CourseView.as_view(), ),
]


