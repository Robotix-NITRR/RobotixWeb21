# Generated by Django 3.1.7 on 2021-03-14 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]