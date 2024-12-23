# Generated by Django 5.1.3 on 2024-12-16 16:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniWeb_13_024_7', '0010_alter_events_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavorisCours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favoris', models.BooleanField(default=False, null=True, verbose_name='Favoris')),
                ('pdf', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UniWeb_13_024_7.cours', verbose_name='Document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateurs')),
            ],
            options={
                'verbose_name': '#Favoris-Cours',
                'verbose_name_plural': '#Favoris-Cours',
                'unique_together': {('user', 'pdf')},
            },
        ),
        migrations.CreateModel(
            name='FavorisDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favoris', models.BooleanField(default=False, null=True, verbose_name='Favoris')),
                ('pdf', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UniWeb_13_024_7.document', verbose_name='Document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateurs')),
            ],
            options={
                'verbose_name': '#Favoris-Document',
                'verbose_name_plural': '#Favoris-Document',
                'unique_together': {('user', 'pdf')},
            },
        ),
    ]
