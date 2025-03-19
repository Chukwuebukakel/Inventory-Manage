from django.contrib import admin
from .models import Product, Order, Branch, Stock, Transaction
from django.contrib.auth.models import Group 


admin.site.site_header = 'Diabond Dashboard'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'price',)
    list_filter = ['category']
    search_fields = ['name', 'sku']

# 📍 Branch Admin
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "latitude", "longitude", "radius")
    search_fields = ("name",)


# 📊 Stock Admin (Manages Inventory per Branch)
class StockAdmin(admin.ModelAdmin):
    list_display = ("branch", "product", "quantity")
    search_fields = ("product__name", "branch__name")
    list_filter = ("branch",)


# 🛒 Transaction Admin (Sales & Restocking)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("branch", "product", "transaction_type", "quantity", "timestamp")
    search_fields = ("product__name", "branch__name")
    list_filter = ("transaction_type", "branch", "timestamp")


# Register your models here
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Branch)
admin.site.register(Stock)
admin.site.register(Transaction)
# admin.site.unregister(Group)
