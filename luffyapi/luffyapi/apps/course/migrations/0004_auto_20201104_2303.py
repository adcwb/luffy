# Generated by Django 2.2.16 on 2020-11-04 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20201104_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_video',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='video', verbose_name='封面video'),
        ),
    ]
