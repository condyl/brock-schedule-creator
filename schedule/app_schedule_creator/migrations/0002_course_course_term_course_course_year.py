# Generated by Django 5.0.5 on 2024-05-08 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_schedule_creator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_term',
            field=models.CharField(default='spring', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='course_year',
            field=models.IntegerField(default=2024),
            preserve_default=False,
        ),
    ]
