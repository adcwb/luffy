# 必须定义 Command 类，继承自 BaseCommand 或其子类。
from django.core.management.base import BaseCommand, CommandError
from users import models
from faker import Faker
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    """
    help:
        这个变量可写可不写，这个变量的作用是在使用命令的-h或--help参数时会显示出来的文字，在这里我们可以写入这条命令的作用，描述。
    add_argument:
        给自定义的命令添加参数
    handle函数：
        这个函数是必须写的函数，我们使用这条命令的时候就会执行这个函数里面的代码。
    """
    help = 'Create users in batch'

    def add_arguments(self, parser):
        parser.add_argument('num', nargs='+', type=int)

    def handle(self, *args, **options):
        """
        username, password, email, phone, is_staff = 1
        :param args:
        :param options:
        :return:
        """
        faker = Faker(locale="zh_CN")
        try:
            user_list = []
            num = options['num']
            print(num)
            for i in range(num[0]):
                print(i)
                user_obj = models.User(
                    username=faker.name(),
                    password=make_password(faker.password()),
                    email=faker.email(),
                    phone=faker.phone_number(),
                    is_staff=1
                )
                print(user_obj)
                user_list.append(user_obj)
            print(user_list)
            models.User.objects.bulk_create(user_list)
        except:
            raise CommandError('%s用户名已存在请重试' % faker.name())

        self.stdout.write('用户创建成功')
