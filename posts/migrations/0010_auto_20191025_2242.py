# Generated by Django 2.2.1 on 2019-10-25 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20191025_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphics',
            name='graphicsName',
            field=models.CharField(blank=True, max_length=10000000, null=True),
        ),
    ]
