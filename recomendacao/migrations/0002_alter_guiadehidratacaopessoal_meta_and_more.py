# Generated by Django 4.1.5 on 2023-01-10 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recomendacao", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guiadehidratacaopessoal",
            name="meta",
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name="guiadehidratacaopessoal",
            name="recomendacao",
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]