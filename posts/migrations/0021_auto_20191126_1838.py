# Generated by Django 2.2.4 on 2019-11-26 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genuineblogers',
            name='followers',
        ),
        migrations.AddField(
            model_name='account',
            name='followers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
