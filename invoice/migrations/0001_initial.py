# Generated by Django 3.1.2 on 2020-10-20 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=15)),
                ('user_type', models.CharField(choices=[('ADMIN', 'Admin'), ('NORMAL', 'Normal')], default='NORMAL', max_length=6)),
            ],
            options={
                'db_table': 'user_details',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('image', models.ImageField(upload_to='')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.userdetail')),
            ],
            options={
                'db_table': 'invoices',
            },
        ),
    ]