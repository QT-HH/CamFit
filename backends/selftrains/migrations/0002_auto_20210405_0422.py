# Generated by Django 3.1.7 on 2021-04-04 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selftrains', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='selftrain',
            name='thumbnail2',
            field=models.ImageField(blank=True, upload_to='%Y%m%d'),
        ),
        migrations.AddField(
            model_name='selftrain',
            name='thumbnail3',
            field=models.ImageField(blank=True, upload_to='%Y%m%d'),
        ),
    ]
