# Generated by Django 5.2.1 on 2025-05-24 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cliente',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
