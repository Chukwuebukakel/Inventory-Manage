from django import forms
from .models import Product, Order, Stock, Transaction, Invoice, InvoiceItem, Branch
from django.forms import inlineformset_factory
from .models import Sale

from decimal import Decimal
import re

from .models import Loan


def clean_price(price_str):
    """Remove currency symbols, commas, and convert to Decimal."""
    cleaned_price = re.sub(r'[^\d.]', '', price_str)  # Remove non-numeric characters except "."
    return Decimal(cleaned_price) if cleaned_price else Decimal("0.00")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price']

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if isinstance(price, str):  # Ensure it's a string before cleaning
            price = clean_price(price)
        return price    
        

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity', 'discount']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['branch', 'product', 'quantity']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'from_branch', 'to_branch', 'transaction_type', 'quantity', 'price']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer_name']

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'unit_price']


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["product", "user", "quantity"]


# Formset for multiple invoice items
InvoiceItemFormSet = inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, extra=3, can_delete=True)