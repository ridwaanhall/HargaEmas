from django.db import models
from django.utils import timezone

class Balance(models.Model):
    date_time = models.DateTimeField(default=timezone.now, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    @classmethod
    def recalculate(cls):
        """ Recalculate total income, expenses, and balance across all transactions """
        from django.apps import apps  # Lazy import to avoid circular dependency
        Income = apps.get_model('incomeapp', 'Income')
        Expense = apps.get_model('expenseapp', 'Expense')

        total_income = Income.objects.aggregate(total=models.Sum('amount'))['total'] or 0
        total_expense = Expense.objects.aggregate(total=models.Sum('amount'))['total'] or 0

        balance, created = cls.objects.get_or_create(date_time=timezone.now().date())

        balance.income = total_income
        balance.expense = total_expense
        balance.balance = total_income - total_expense
        balance.save()
