# Generated by Django 4.0.2 on 2022-10-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dm',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at'),
        ),
    ]
