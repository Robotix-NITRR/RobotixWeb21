# Generated by Django 3.2 on 2021-06-08 16:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0002_auto_20210607_2211'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuestionsForRecruitment',
            new_name='Questions',
        ),
        migrations.AlterField(
            model_name='formresponses',
            name='options_answer_selected',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('All', 'All'), ('Web', 'Web'), ('Core', 'Core'), ('Design', 'Design'), ('Docs', 'Docs'), ('PR', 'PR')], max_length=100), blank=True, null=True, size=4),
        ),
    ]
