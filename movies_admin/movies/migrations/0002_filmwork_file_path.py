# Generated by Django 4.2.11 on 2024-04-03 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmwork',
            name='file_path',
            field=models.TextField(blank=True, null=True, verbose_name='file_path'),
        ),
    ]
