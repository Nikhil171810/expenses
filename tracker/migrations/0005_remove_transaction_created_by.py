# Generated by Django 4.2.11 on 2024-08-06 08:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0004_alter_transaction_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="created_by",
        ),
    ]
