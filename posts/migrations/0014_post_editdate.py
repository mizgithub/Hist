# Generated by Django 2.2.1 on 2019-10-30 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_post_posttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='editDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
