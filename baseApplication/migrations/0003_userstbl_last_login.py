# Generated by Django 5.0.2 on 2024-04-04 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseApplication', '0002_alter_userstbl_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstbl',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]