# Generated by Django 5.0.6 on 2024-07-18 03:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sets', '0003_sets_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('owner_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sets.sets')),
            ],
        ),
    ]