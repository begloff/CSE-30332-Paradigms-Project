# Generated by Django 4.0.5 on 2022-12-01 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_post_company_post_expiration_date_post_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
        migrations.AddField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]