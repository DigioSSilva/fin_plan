# Generated by Django 4.2.16 on 2024-10-22 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planejamento", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="categoria",
            name="montante_plan",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]