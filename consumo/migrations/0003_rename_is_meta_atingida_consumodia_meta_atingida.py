# Generated by Django 4.1.5 on 2023-01-14 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("consumo", "0002_consumodia_meta"),
    ]

    operations = [
        migrations.RenameField(
            model_name="consumodia",
            old_name="is_meta_atingida",
            new_name="meta_atingida",
        ),
    ]