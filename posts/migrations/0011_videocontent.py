# Generated by Django 2.2.1 on 2019-10-26 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20191025_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoName', models.CharField(blank=True, max_length=100000000, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
            ],
        ),
    ]
