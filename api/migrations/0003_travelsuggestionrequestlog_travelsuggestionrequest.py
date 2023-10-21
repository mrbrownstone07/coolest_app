# Generated by Django 4.2.6 on 2023-10-21 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_forecast"),
    ]

    operations = [
        migrations.CreateModel(
            name="TravelSuggestionRequestLog",
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
                ("request_ip", models.CharField(blank=True, max_length=55, null=True)),
                ("location", models.CharField(blank=True, max_length=55, null=True)),
                ("destination", models.CharField(blank=True, max_length=55, null=True)),
                ("travel_date", models.CharField(blank=True, max_length=55, null=True)),
                ("response", models.TextField(blank=True, null=True)),
                ("error", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="TravelSuggestionRequest",
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
                ("travel_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("processed", models.BooleanField(default=False)),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="TravelSuggestionDestination",
                        to="api.district",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="TravelSuggestionLocation",
                        to="api.district",
                    ),
                ),
            ],
        ),
    ]
