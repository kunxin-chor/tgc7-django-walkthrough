# Generated by Django 2.2.13 on 2020-09-08 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_auto_20200908_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='email',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
