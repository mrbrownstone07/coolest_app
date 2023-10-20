# Generated by Django 4.2.6 on 2023-10-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="District",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("division_id", models.IntegerField()),
                ("longitude", models.DecimalField(decimal_places=2, max_digits=4)),
                ("latitude", models.DecimalField(decimal_places=2, max_digits=4)),
                ("name", models.CharField(db_index=True, max_length=55, unique=True)),
            ],
        ),
    ]
