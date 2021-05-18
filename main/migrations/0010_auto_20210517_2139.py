# Generated by Django 3.2.1 on 2021-05-17 18:39

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_company_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='content_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='title_en',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='title_ru',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='description_en',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='description_ru',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='theme_en',
            field=models.CharField(choices=[('EL', 'Electronic'), ('IT', 'IT'), ('ED', 'Education'), ('CH', 'Charity'), ('GP', 'GreenPeace')], default='IT', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='theme_ru',
            field=models.CharField(choices=[('EL', 'Electronic'), ('IT', 'IT'), ('ED', 'Education'), ('CH', 'Charity'), ('GP', 'GreenPeace')], default='IT', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='title_en',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='title_ru',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
