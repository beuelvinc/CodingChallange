# Generated by Django 4.1.7 on 2023-03-02 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socket_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordinates',
            name='user_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
