# Generated by Django 3.1.2 on 2020-10-20 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='username',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
