# Generated by Django 5.0.3 on 2024-06-22 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseApplication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertbl',
            name='email',
            field=models.EmailField(max_length=70, unique=True),
        ),
    ]
