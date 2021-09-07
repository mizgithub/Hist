# Generated by Django 2.2.1 on 2019-11-26 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_remove_post_posttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenuineBlogers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.IntegerField()),
                ('date', models.DateField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Account')),
            ],
        ),
    ]
