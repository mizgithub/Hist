# Generated by Django 2.2.4 on 2019-10-21 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
