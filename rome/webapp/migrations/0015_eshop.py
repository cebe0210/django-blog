# Generated by Django 5.0.1 on 2024-01-30 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_alter_article_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='img/eshop/')),
                ('stock', models.IntegerField()),
                ('price', models.IntegerField()),
                ('active', models.BooleanField(choices=[(True, 'Actif'), (False, 'Inactif')], default=True)),
            ],
        ),
    ]