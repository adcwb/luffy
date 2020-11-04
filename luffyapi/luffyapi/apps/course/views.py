from django.shortcuts import render
from . import models
# Create your views here.

from rest_framework.generics import ListAPIView
from .serializers import CourseCategoryModelSerializer, CourseModelsSerializer
from .pagenations import StandardPageNumberPagination


class CategoryView(ListAPIView):

    queryset = models.CourseCategory.objects.filter(is_deleted=False,is_show=True)
    serializer_class = CourseCategoryModelSerializer


# class CourseView(ListAPIView):
#     queryset = models.Course.objects.filter(is_deleted=False,is_show=True).order_by('id')
#     serializer_class = CourseModelsSerializer


# 加过滤
class CourseView(ListAPIView):
    queryset = models.Course.objects.filter(is_deleted=False,is_show=True).order_by('id')
    serializer_class = CourseModelsSerializer
    filter_fields = ('course_category', )
    pagination_class = StandardPageNumberPagination
