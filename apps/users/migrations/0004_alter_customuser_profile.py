# Generated by Django 3.2 on 2021-05-31 16:22

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210521_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile',
            field=models.ImageField(blank=True, upload_to=users.models.PathAndRename('members/')),
        ),
    ]
