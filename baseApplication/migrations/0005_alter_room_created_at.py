# Generated by Django 5.0.3 on 2024-06-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseApplication', '0004_remove_chatroom_members_admin_room_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='created_at',
            field=models.DateTimeField(default=True),
        ),
    ]