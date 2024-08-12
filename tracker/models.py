from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('home_expenditure', 'Home Expenditure'),
        ('personal_expense', 'Personal Expense'),
        ('bills', 'Bills'),
        ('others', 'Others'),
    ]

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)   
    date = models.DateTimeField(help_text="Enter date in YYYY-MM-DD format")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    DisplayFields = ['id', 'description', 'amount', 'category', 'date', 'created_by']

    def __str__(self):
        return f"{self.description} - {self.amount}"
    

    class Meta:
        ordering = ('description',)

