from django.db import models
from django.contrib.auth.models import AbstractUser
from luffyapi.utils.models import BaseModel


# Create your models here.


class User(AbstractUser):
    """用户模型类"""
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='手机号码')
    avatar = models.ImageField(upload_to='avatar', verbose_name='用户头像', null=True, blank=True)
    wechat = models.CharField(max_length=16, null=True, blank=True)
    credit = models.IntegerField(default=0, blank=True, verbose_name="贝里")

    class Meta:
        db_table = 'ly_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Credit(BaseModel):
    """积分流水"""
    OPERA_OPION = (
        (1, "赚取"),
        (2, "消费"),
    )
    user = models.ForeignKey("User", related_name="user_credit", on_delete=models.CASCADE, verbose_name="用户")
    opera = models.SmallIntegerField(choices=OPERA_OPION, verbose_name="操作类型")
    number = models.SmallIntegerField(default=0, verbose_name="积分数值")

    class Meta:
        db_table = 'ly_credit'
        verbose_name = '积分流水'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s %s %s 贝壳" % (self.user.username, self.OPERA_OPION[self.opera][1], self.number)
