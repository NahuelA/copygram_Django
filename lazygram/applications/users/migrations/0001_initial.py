# Generated by Django 4.0.2 on 2022-10-25 15:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biography', models.CharField(blank=True, default='', max_length=350)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='uploads/users_profile')),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('website', models.URLField(blank=True, default='')),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: +999999999. Up to 15 digits allowed.', regex='\\+?1?\\d{9,15}$')])),
                ('posts_count', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Username')),
            ],
            options={
                'verbose_name_plural': 'Profiles',
            },
            managers=[
                ('manager_object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='FollowingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following_length', models.PositiveIntegerField(default=0)),
                ('following', models.ManyToManyField(related_name='Following', to='users.Profile', verbose_name='Following')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Following',
            },
        ),
        migrations.CreateModel(
            name='FollowersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers_length', models.PositiveIntegerField(default=0)),
                ('followers', models.ManyToManyField(related_name='followers', to='users.Profile', verbose_name='Followers')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Followers',
            },
        ),
    ]
