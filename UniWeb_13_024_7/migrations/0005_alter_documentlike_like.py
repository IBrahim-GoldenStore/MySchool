# Generated by Django 5.1.3 on 2024-12-13 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniWeb_13_024_7', '0004_documentlike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentlike',
            name='like',
            field=models.BooleanField(default=True, verbose_name='like'),
        ),
    ]
