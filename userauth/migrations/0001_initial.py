# Generated by Django 4.2.11 on 2024-07-07 16:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('password', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+234XXXXXXXXXX', or '234XXXXXXXXXX', or '0XXXXXXXXXX' .", regex='((^+)(234){1}\\d{10})|((^234)\\d{10})|((^0)(7|8|9){1}(0|1){1}[0–9]{8})')])),
            ],
        ),
        migrations.CreateModel(
            name='UserOrganisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userauth.organisation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userauth.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='organisations',
            field=models.ManyToManyField(related_name='users', through='userauth.UserOrganisation', to='userauth.organisation'),
        ),
    ]
