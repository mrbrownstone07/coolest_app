# Generated by Django 4.2.6 on 2023-10-21 12:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_travelsuggestionrequest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="forecast",
            name="temperature",
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=4),
        ),
    ]
