# Generated by Django 3.2.1 on 2021-05-12 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
    ]
