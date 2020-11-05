from rest_framework import serializers
from . import models


class CourseCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id', 'name']


class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['name', 'role', 'title', 'signature']


class CourseModelsSerializer(serializers.ModelSerializer):

    teacher = TeacherModelSerializer()  # 将外键关联的属性指定为关联表的序列化器对象，就能拿到关联表序列化出来的所有数据，还需要在fields中指定一下，注意，名称必须和外键属性名称相同

    class Meta:
        model = models.Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher",
                  "get_lessons"]  # teacher外键属性默认拿的是id值


class CourseDetailModelSerializer(serializers.ModelSerializer):
    # 序列化器嵌套
    teacher = TeacherModelSerializer()  # 将外键关联的属性指定为关联表的序列化器对象，就能拿到关联表序列化出来的所有数据，还需要在fields中指定一下，注意，名称必须和外键属性名称相同

    class Meta:
        model = models.Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher",
                  "level_name", "course_video", 'new_brief']  # teacher外键属性默认拿的是id值


class CourseLessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseLesson
        fields = ['name', 'section_link', 'duration', 'free_trail', 'lesson']


class CourseChapterModelSerializer(serializers.ModelSerializer):
    coursesections = CourseLessonModelSerializer(many=True)  # fang

    class Meta:
        model = models.CourseChapter
        fields = ['chapter', 'name', 'coursesections']
