# Generated by Django 4.2.16 on 2024-10-29 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
