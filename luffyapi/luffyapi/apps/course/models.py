from django.db import models
from luffyapi.utils.models import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField
from luffyapi.settings import constants


# Create your models here.
class CourseCategory(BaseModel):
    """
    课程分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "ly_course_category"
        verbose_name = "课程分类"
        verbose_name_plural = "课程分类"

    def __str__(self):
        return "%s" % self.name


class Course(BaseModel):
    """
    专题课程
    """
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )

    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="course", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_video = models.FileField(upload_to='video', verbose_name='封面video', blank=True, null=True, max_length=255)
    # 费用类型字段是为了后期一些其他功能拓展用的，现在可以先不用，或者去掉它，目前我们项目用不到
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # 这个字段是课程详情页里面展示的，并且详情介绍里面用户将来可能要上传一些图片之类的，所以我们会潜入富文本编辑器，让用户填写数据的时候可以上传图片啊、写标题啊、css、html等等内容
    brief = RichTextUploadingField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)

    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)

    # 课件资料的存放路径
    attachment_path = models.FileField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    course_category = models.ForeignKey("CourseCategory", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数", default=0)
    lessons = models.IntegerField(verbose_name="总课时数量", default=0)

    # 总课时数量可能10个，但是目前之更新了3个，就跟小说、电视剧连载似的。
    pub_lessons = models.IntegerField(verbose_name="课时更新数量", default=0)

    # 课程原价
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0,
                                help_text='如果填写的价格为0，那么表示当前课程在购买的时候，没有永久有效的期限。')
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    class Meta:
        db_table = "ly_course"
        verbose_name = "专题课程"
        verbose_name_plural = "专题课程"

    def __str__(self):
        return "%s" % self.name

    # 通过课程对象获取所有课程列表页中要展示的课时信息
    def get_lessons(self):
        chapters = self.coursechapters.all()
        lession_list = []
        for chapter in chapters:
            lessons = chapter.coursesections.filter(is_show_list=True, is_show=True, is_deleted=False)
            for lesson in lessons:
                lession_list.append({
                    'name': lesson.name,
                    'free_trail': lesson.free_trail,
                    'lesson': lesson.lesson,
                })
        return lession_list[:4]

    def level_name(self):

        return self.get_level_display()

    def new_brief(self):
        data = self.brief
        server_addr = constants.SERVER_ADDR
        data = data.replace('src="/media', f'class="img_xx" src="{server_addr}/media')
        return data

    def activity(self):
        import datetime
        now = datetime.datetime.now()
        activity_list = self.activeprices.filter(is_show=True, is_deleted=False, active__start_time__lte=now,
                                                 active__end_time__gte=now)
        return activity_list

    # 优惠类型名称
    def discount_name(self):

        dis_name = ''
        a = self.activity()
        if a:
            discount_n_list = []
            for i in a:
                discount_n = i.discount.discount_type.name
                discount_n_list.append(discount_n)
            dis_name = discount_n_list[0]

        return dis_name

    # 真实价格计算
    def real_price(self,expire_id=0):
        price = float(self.price)


        if expire_id > 0:
            expire_obj = self.course_expire.get(id=expire_id)
            price = float(expire_obj.price)

        r_price = price
        a = self.activity()
        if a:
            sale = a[0].discount.sale
            condition_price = a[0].discount.condition
            # 限时免费
            if not sale.strip():
                r_price = 0

            # 限时折扣  *0.5
            elif '*' in sale.strip():
                if price >= condition_price:
                    _, d = sale.split('*')
                    r_price = price * float(d)
            # 限时减免  -100
            elif sale.strip().startswith('-'):
                if price >= condition_price:
                    _, d = sale.split('-')
                    r_price = price - float(d)
            # 满减
            # '''
            #     满100-10
            #     满300 - 50
            #     满600 - 100
            #     满200-25
            #
            # '''
            elif '满' in sale:
                if price >= condition_price:
                    l1 = sale.split('\r\n')
                    dis_list = []  #10 50  25
                    for i in l1:
                        a, b = i[1:].split('-')

                        #400
                        if price >= float(a):
                            dis_list.append(float(b))

                    max_dis = max(dis_list)
                    r_price = price - max_dis

        return r_price

    # 活动倒计时时间戳
    def left_time(self):
        import datetime
        now = datetime.datetime.now().timestamp()
        left_t = 0
        a = self.activity()
        if a:
            end_time = a[0].active.end_time.timestamp()
            left_t = end_time - now

        return left_t

    # 获取课程有效期
    def get_expire(self):
        expire_list = self.course_expire.all()
        data = []
        for expire in expire_list:
            data.append({
                'id': expire.id,
                'expire_text': expire.expire_text,
                'price': expire.price,
            })

        # 当价格为0时，没有永久有效这一项，其他的都有
        if self.price > 0:
            data.append({
                'id': 0,
                'expire_text': '永久有效',
                'price': self.price,
            })

        return data


class Teacher(BaseModel):
    """讲师、导师表"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="讲师title")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name="讲师封面")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    class Meta:
        db_table = "ly_teacher"
        verbose_name = "讲师导师"
        verbose_name_plural = "讲师导师"

    def __str__(self):
        return "%s" % self.name


class CourseChapter(BaseModel):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "ly_course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = "课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseLesson(BaseModel):
    """课程课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )

    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,
                                verbose_name="课程章节")
    name = models.CharField(max_length=128, verbose_name="课时标题")
    # orders = models.PositiveSmallIntegerField(verbose_name="课时排序") #在basemodel里面已经有了排序了
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")

    duration = models.CharField(verbose_name="视频时长", blank=True, null=True,
                                max_length=32)  # 仅在前端展示使用，所以直接让上传视频的用户直接填写时长进来就可以了。

    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)

    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)

    course = models.ForeignKey('Course', related_name='course_lesson', verbose_name='课程', on_delete=models.CASCADE,
                               null=True, blank=True)

    is_show_list = models.BooleanField(verbose_name='是否推荐到课程列表', default=False)  # 知否在课程列表页展示

    lesson = models.IntegerField(verbose_name="第几课时")

    class Meta:
        db_table = "ly_course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = "课程课时"

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


"""价格相关的模型"""


class CourseDiscountType(BaseModel):
    """课程优惠类型"""
    name = models.CharField(max_length=32, verbose_name="优惠类型名称")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_course_discount_type"
        verbose_name = "课程优惠类型"
        verbose_name_plural = "课程优惠类型"

    def __str__(self):
        return "%s" % (self.name)


class CourseDiscount(BaseModel):
    """课程优惠模型"""
    discount_type = models.ForeignKey("CourseDiscountType", on_delete=models.CASCADE, related_name='coursediscounts',
                                      verbose_name="优惠类型")
    condition = models.IntegerField(blank=True, default=0, verbose_name="满足优惠的价格条件",
                                    help_text="设置参与优惠的价格门槛，表示商品必须在xx价格以上的时候才参与优惠活动，<br>如果不填，则不设置门槛")
    # 因为有的课程不足100，你减免100，还亏钱了
    sale = models.TextField(verbose_name="优惠公式", blank=True, null=True, help_text="""
    不填表示免费；<br>
    *号开头表示折扣价，例如*0.82表示八二折；<br>
    -号开头则表示减免，例如-20表示原价-20；<br>
    如果需要表示满减,则需要使用 原价-优惠价格,例如表示课程价格大于100,优惠10;大于200,优惠25,格式如下:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-25<br>
    """)

    class Meta:
        db_table = "ly_course_discount"
        verbose_name = "价格优惠策略"
        verbose_name_plural = "价格优惠策略"

    def __str__(self):
        return "价格优惠:%s,优惠条件:%s,优惠值:%s" % (self.discount_type.name, self.condition, self.sale)


class Activity(BaseModel):
    """优惠活动"""
    name = models.CharField(max_length=150, verbose_name="活动名称")
    start_time = models.DateTimeField(verbose_name="优惠策略的开始时间")
    end_time = models.DateTimeField(verbose_name="优惠策略的结束时间")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_activity"
        verbose_name = "商品活动"
        verbose_name_plural = "商品活动"

    def __str__(self):
        return self.name


class CoursePriceDiscount(BaseModel):
    """课程与优惠策略的关系表"""
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="activeprices", verbose_name="课程")
    active = models.ForeignKey("Activity", on_delete=models.DO_NOTHING, related_name="activecourses", verbose_name="活动")
    discount = models.ForeignKey("CourseDiscount", on_delete=models.CASCADE, related_name="discountcourse",
                                 verbose_name="优惠折扣")

    class Meta:
        db_table = "ly_course_price_dicount"
        verbose_name = "课程与优惠策略的关系表"
        verbose_name_plural = "课程与优惠策略的关系表"

    def __str__(self):
        return "课程：%s，优惠活动: %s,开始时间:%s,结束时间:%s" % (
            self.course.name, self.active.name, self.active.start_time, self.active.end_time)


class CourseExpire(BaseModel):
    """课程有效期模型"""
    # 后面可以在数据库把course和expire_time字段设置为联合索引
    course = models.ForeignKey("Course", related_name='course_expire', on_delete=models.CASCADE, verbose_name="课程名称")

    # 有效期限，天数
    expire_time = models.IntegerField(verbose_name="有效期", null=True, blank=True, help_text="有效期按天数计算")

    # 一个月有效等等
    expire_text = models.CharField(max_length=150, verbose_name="提示文本", null=True, blank=True)
    # 每个有效期的价格
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程价格", default=0)

    class Meta:
        db_table = "ly_course_expire"
        verbose_name = "课程有效期"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "课程：%s，有效期：%s，价格：%s" % (self.course, self.expire_text, self.price)
