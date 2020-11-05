from django.shortcuts import render
from . import models
# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import CourseCategoryModelSerializer, CourseModelsSerializer, CourseDetailModelSerializer, \
    CourseChapterModelSerializer

from rest_framework.generics import ListAPIView
from .pagenations import StandardPageNumberPagination


class CategoryView(ListAPIView):
    queryset = models.CourseCategory.objects.filter(is_deleted=False, is_show=True)
    serializer_class = CourseCategoryModelSerializer


# class CourseView(ListAPIView):
#     queryset = models.Course.objects.filter(is_deleted=False,is_show=True).order_by('id')
#     serializer_class = CourseModelsSerializer


# 加过滤
class CourseView(ListAPIView):
    queryset = models.Course.objects.filter(is_deleted=False, is_show=True).order_by('id')
    serializer_class = CourseModelsSerializer
    filter_fields = ('course_category',)
    pagination_class = StandardPageNumberPagination


class CourseDetailView(RetrieveAPIView):
    queryset = models.Course.objects.filter(is_deleted=False, is_show=True)
    serializer_class = CourseDetailModelSerializer


from django_filters.rest_framework import DjangoFilterBackend


class ChapterView(ListAPIView):
    queryset = models.CourseChapter.objects.filter(is_deleted=False, is_show=True)
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend, ]
    filter_fields = ('course',)
    # /chapter/?course=1
