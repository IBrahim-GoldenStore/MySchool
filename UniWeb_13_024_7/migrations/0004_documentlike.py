# Generated by Django 5.1.3 on 2024-12-13 08:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniWeb_13_024_7', '0003_remove_cours_dislike_remove_document_dislike_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='like')),
                ('pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniWeb_13_024_7.document', verbose_name='Document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'unique_together': {('user', 'pdf')},
            },
        ),
    ]
