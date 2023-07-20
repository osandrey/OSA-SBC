# Generated by Django 4.2.1 on 2023-06-10 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='citizen',
            name='telephone_num',
            field=models.CharField(max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
