import xadmin
from .models import Course
from .models import CourseCategory
from .models import Teacher
from .models import CourseChapter
from .models import CourseLesson

# 把当前新增的课程模型注册到xadmin里面.


class CourseCategoryModelAdmin(object):
    """课程分类模型管理类"""
    pass


xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


class CourseModelAdmin(object):
    """课程模型管理类"""
    pass


xadmin.site.register(Course, CourseModelAdmin)


class TeacherModelAdmin(object):
    """老师模型管理类"""
    pass


xadmin.site.register(Teacher, TeacherModelAdmin)


class CourseChapterModelAdmin(object):
    """课程章节模型管理类"""
    pass


xadmin.site.register(CourseChapter, CourseChapterModelAdmin)


class CourseLessonModelAdmin(object):
    """课程课时模型管理类"""
    pass


xadmin.site.register(CourseLesson, CourseLessonModelAdmin)
