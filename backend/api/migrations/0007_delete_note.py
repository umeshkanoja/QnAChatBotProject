# Generated by Django 5.1.2 on 2024-10-26 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_embedding_text'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Note',
        ),
    ]
