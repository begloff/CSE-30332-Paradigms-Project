# Generated by Django 4.1.2 on 2022-12-07 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='declined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]