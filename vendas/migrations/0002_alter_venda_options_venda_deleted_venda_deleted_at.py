# Generated by Django 5.2.1 on 2025-05-29 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venda',
            options={'ordering': ['-data_venda']},
        ),
        migrations.AddField(
            model_name='venda',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Excluído'),
        ),
        migrations.AddField(
            model_name='venda',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão'),
        ),
    ]
