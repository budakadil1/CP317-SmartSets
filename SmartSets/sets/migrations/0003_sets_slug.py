# Generated by Django 5.0.6 on 2024-07-18 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sets', '0002_alter_sets_shared_with'),
    ]

    operations = [
        migrations.AddField(
            model_name='sets',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]