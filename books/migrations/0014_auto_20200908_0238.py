# Generated by Django 2.2.13 on 2020-09-08 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_book_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
