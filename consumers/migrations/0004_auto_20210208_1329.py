# Generated by Django 3.1.5 on 2021-02-08 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumers', '0003_auto_20210207_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='gender',
            field=models.CharField(choices=[('O', 'Other'), ('M', 'male'), ('F', 'female')], default='F', max_length=1),
        ),
    ]
