# Generated by Django 4.1.2 on 2022-12-05 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_candidate_id_alter_candidate_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='interests',
            field=models.ManyToManyField(to='users.candidate'),
        ),
    ]
