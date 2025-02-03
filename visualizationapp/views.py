from django.shortcuts import render
from incomeapp.models import Income
from expenseapp.models import Expense
from balanceapp.models import Balance
import matplotlib.pyplot as plt
import io
import urllib, base64

def generate_chart():
    # Fetch data
    incomes = Income.objects.all()
    expenses = Expense.objects.all()
    balances = Balance.objects.all()

    # Data processing and plotting
    dates = [income.date for income in incomes]
    income_values = [income.amount for income in incomes]
    expense_values = [expense.amount for expense in expenses]
    balance_values = [balance.balance for balance in balances]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, income_values, label='Income')
    plt.plot(dates, expense_values, label='Expense')
    plt.plot(dates, balance_values, label='Balance')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Financial Overview')
    plt.legend()

    # Save plot to a StringIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode image to base64 string
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    return graph

def visualize(request):
    chart = generate_chart()
    return render(request, 'visualizationapp/visualize.html', {'chart': chart})
