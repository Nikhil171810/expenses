# Generated by Django 4.2.11 on 2024-08-05 09:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tracker", "0002_category_expense_delete_transaction"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Expense",
            new_name="Transaction",
        ),
    ]
