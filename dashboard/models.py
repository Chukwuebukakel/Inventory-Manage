from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from django.utils.timezone import now
from django.core.exceptions import ValidationError




import uuid


CATEGORY = (
    ('Interior Panels', 'Interior Panels'),
    ('Exterior Panels', 'Exterior Panels'),
    ('Aluco Board', 'Aluco Board'),
    ('Wooden Door', 'Wooden Door'),
    ('Cast Door', 'Cast Door'),
    ('Sintered Stone', 'Sintered Stone'),
    ('SPC Flooring Tile', 'SPC Flooring Tile'),
    ('UV Marble Sheet', 'UV Marble Sheet'),
    ('Sandwich Panel', 'Sandwich Panel'),
    ('3D Foam Sticker', '3D Foam Sticker'),
    ('PU Stone', 'PU Stone'),
    ('WPC Interlocking', 'WPC Interlocking'),
    ('PS Cornice', 'PS Cornice'),
    ('PS Skirting', 'PS Skirting'),
    ('Tiles', 'Tiles'),
    ('Artificial Grass', 'Artificial Grass'),
    ('Toilet', 'Toilet'),
    ('Roofing Sheets', 'Roofing Sheets'),
    ('Railings', 'Railings'),
    
    
    
    
    
    







)


# SKU Generator
def generate_sku():
    return str(uuid.uuid4())[:8]  # Generates a unique 8-character SKU

 # Branch Model
class Branch(models.Model):
    name = models.CharField(max_length=100)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    radius = models.FloatField(default=0.05, null=True)  # Radius in km for geofencing
    
    class Meta:
        verbose_name_plural = 'Branch'

    def __str__(self):
        return self.name
    


class Attendance(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    date = models.DateField(default=now)

    def __str__(self):
        return f"{self.staff.username} - {self.date}"
    



class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True) 
    quantity = models.PositiveIntegerField(null=True)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='NGN', null=True)
    quantity_in_stock = models.PositiveIntegerField(default=0, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True, default=generate_sku, blank=True) # Stock Keeping Unit
       

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return f"{self.name} -- {self.sku} -- ₦{self.price.amount:,.2f}"
    

class Loan(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    issued_date = models.DateTimeField(default=now, null=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def mark_as_returned(self):
        if not self.is_returned:
            self.is_returned = True
            self.returned_date = now()
            self.product.quantity_in_stock += self.quantity  # Add back to stock
            self.product.save()
            self.save()

    def __str__(self):
        return f"{self.product.name} - {self.user.username} ({'Returned' if self.is_returned else 'On Loan'})"

    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveBigIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Order'

 
    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'


  
  
# Stock Model    
class Stock(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.branch.name} - {self.product.name}: {self.quantity} items"

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('TRANSFER', 'Branch Transfer'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    from_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="transfer_from", null=True, blank=True)
    to_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="transfer_to", null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, null=True)
    quantity = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price

        if self.transaction_type == 'IN':
            stock, created = Stock.objects.get_or_create(product=self.product, branch=self.from_branch)
            stock.quantity += self.quantity
            stock.save()

        elif self.transaction_type == 'OUT':
            stock = Stock.objects.filter(product=self.product, branch=self.from_branch).first()
            if not stock or stock.quantity < self.quantity:
                raise ValueError("Not enough stock available!")
            stock.quantity -= self.quantity
            stock.save()

        elif self.transaction_type == 'TRANSFER':
            from_stock = Stock.objects.filter(product=self.product, branch=self.from_branch).first()
            if not from_stock or from_stock.quantity < self.quantity:
                raise ValueError("Not enough stock in the sending branch!")
            from_stock.quantity -= self.quantity
            from_stock.save()

            to_stock, created = Stock.objects.get_or_create(product=self.product, branch=self.to_branch)
            to_stock.quantity += self.quantity
            to_stock.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} ({self.quantity})"



class Invoice(models.Model):
    customer_name = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Invoice {self.id} - {self.customer_name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('dashboard.Product', on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Invoice {self.invoice.id})"
    



class Sale(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)  # Discount applied
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)
    timestamp = models.DateTimeField(default=now, null=True)

    def save(self, *args, **kwargs):
        """Calculate total price after discount."""
        product_price = self.product.price * self.quantity
        self.total_price = product_price - self.discount  # Apply discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.staff.username} - {self.product.name} ({self.quantity})"
