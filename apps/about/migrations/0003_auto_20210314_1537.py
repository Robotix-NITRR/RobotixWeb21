# Generated by Django 3.1.7 on 2021-03-14 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_team'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Convenor',
        ),
        migrations.DeleteModel(
            name='Coordinator',
        ),
        migrations.DeleteModel(
            name='HeadCoordinator',
        ),
        migrations.DeleteModel(
            name='Manager',
        ),
    ]