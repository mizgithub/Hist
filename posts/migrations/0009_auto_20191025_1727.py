# Generated by Django 2.2.1 on 2019-10-25 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20191025_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphics',
            name='graphicsName',
            field=models.TextField(blank=True, null=True),
        ),
    ]
