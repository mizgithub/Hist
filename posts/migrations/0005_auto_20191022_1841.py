# Generated by Django 2.2.4 on 2019-10-22 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_content',
            name='img_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post_content',
            name='vid_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]