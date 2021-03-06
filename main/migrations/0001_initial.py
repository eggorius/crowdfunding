# Generated by Django 3.2.1 on 2021-05-07 09:35

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('video_url', models.URLField()),
                ('theme', models.CharField(choices=[('EL', 'Electronic'), ('IT', 'IT'), ('ED', 'Education'), ('CH', 'Charity'), ('GP', 'GreenPeace')], default='IT', max_length=2)),
                ('goal', models.DecimalField(decimal_places=2, max_digits=7)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_finish', models.DateField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='companies', to='main.Tag')),
            ],
        ),
    ]
