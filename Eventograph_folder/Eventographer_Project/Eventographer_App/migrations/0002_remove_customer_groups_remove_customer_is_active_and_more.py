# Generated by Django 5.1.6 on 2025-02-24 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventographer_App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='password_hash',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user_permissions',
        ),
        migrations.AddField(
            model_name='customer',
            name='token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
