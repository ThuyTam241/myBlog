# Generated by Django 5.0 on 2023-12-11 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_article_imagelink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.CharField(default='No description', max_length=255),
        ),
    ]
