# Generated by Django 4.0.5 on 2022-12-01 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_recruiter_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiter',
            name='company',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='recruiter',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_title', models.CharField(default='', max_length=100)),
                ('job_type', models.CharField(default='', max_length=100)),
                ('job_city', models.CharField(default='', max_length=100)),
                ('job_state', models.CharField(default='', max_length=100)),
                ('skills', models.CharField(default='', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
