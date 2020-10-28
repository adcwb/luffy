from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    """用户模型类"""
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='手机号码')
    avatar = models.ImageField(upload_to='avatar', verbose_name='用户头像', null=True, blank=True)
    wechat = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        db_table = 'ly_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
