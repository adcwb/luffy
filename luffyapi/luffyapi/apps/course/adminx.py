import xadmin
from .models import Course
from .models import CourseCategory
from .models import Teacher
from .models import CourseChapter
from .models import CourseLesson
from .models import CoursePriceDiscount

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

from .models import CourseDiscountType


class CourseExpireModelAdmin(object):
    """课程与有效期模型管理类"""
    pass


xadmin.site.register(CourseDiscountType, CourseExpireModelAdmin)

from .models import CourseDiscount


class PriceDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    pass


xadmin.site.register(CourseDiscount, PriceDiscountTypeModelAdmin)

from .models import Activity


class PriceDiscountModelAdmin(object):
    """价格优惠公式"""
    pass


xadmin.site.register(Activity, PriceDiscountModelAdmin)




class CoursePriceDiscountModelAdmin(object):
    """商品优惠和活动的关系"""
    pass


xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountModelAdmin)
