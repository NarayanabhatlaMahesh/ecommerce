# Generated by Django 4.2.4 on 2023-09-26 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SportsProduct",
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
                ("name", models.CharField(max_length=100)),
                ("cost", models.BigIntegerField()),
                ("location", models.CharField(max_length=100)),
                ("date", models.DateField()),
                ("removedate", models.DateField()),
                ("supplierName", models.CharField(max_length=100)),
                ("image", models.CharField(max_length=180)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="userAuthenticate",
            fields=[
                (
                    "username",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("password", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=100)),
                ("phonenumber", models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name="userOrder",
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
                ("location", models.CharField(max_length=100)),
                ("ordersActive", models.CharField(max_length=100)),
                ("count", models.BigIntegerField()),
                ("cost", models.BigIntegerField()),
                (
                    "username",
                    models.ForeignKey(
                        db_column="username",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UsualWebsite.userauthenticate",
                    ),
                ),
            ],
        ),
    ]
