# Generated by Django 5.0.3 on 2024-06-23 15:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('username', models.CharField(max_length=70, unique=True)),
                ('email', models.EmailField(max_length=70, unique=True)),
                ('phone_number', models.CharField(max_length=30)),
                ('account_type', models.CharField(max_length=15)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Influencer',
            fields=[
                ('influencer_id', models.AutoField(primary_key=True, serialize=False)),
                ('content_category', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('reference', models.CharField(max_length=150, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('verified', models.BooleanField(default=False)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('platform_id', models.AutoField(primary_key=True, serialize=False)),
                ('platform_name', models.CharField(max_length=100)),
                ('platform_url', models.CharField(max_length=200, unique=True)),
                ('likes', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('subscribers', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('videos', models.IntegerField(default=0)),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseApplication.influencer')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('sponser_id', models.AutoField(primary_key=True, serialize=False)),
                ('content_category', models.CharField(max_length=100, null=True)),
                ('website', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('chat_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseApplication.influencer')),
                ('sponser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseApplication.sponsor')),
            ],
        ),
    ]
