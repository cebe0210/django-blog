# Generated by Django 5.0.1 on 2024-01-27 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_article_image_url_article_use_external_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='carousel_images/')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='itinenaire',
            field=models.BooleanField(choices=[(True, 'Actif'), (False, 'Inactif')], default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='map_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='carousel_images',
            field=models.ManyToManyField(blank=True, null=True, to='webapp.carouselimage'),
        ),
    ]