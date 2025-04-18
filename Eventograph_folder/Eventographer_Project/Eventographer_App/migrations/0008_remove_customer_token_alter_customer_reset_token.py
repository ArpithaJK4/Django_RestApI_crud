# Generated by Django 5.1.6 on 2025-02-28 05:57

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventographer_App', '0007_alter_customer_reset_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='token',
        ),
        migrations.AlterField(
            model_name='customer',
            name='reset_token',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True, unique=True),
        ),
    ]
