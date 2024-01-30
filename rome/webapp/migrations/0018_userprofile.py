# Generated by Django 5.0.1 on 2024-01-30 12:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0017_alter_product_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('address', models.TextField(blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('eshop_points', models.IntegerField(default=0)),
                ('blog_comments_count', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
