
from datetime import date, datetime, timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Stock, Transaction, Invoice, InvoiceItem, Branch
from .forms import ProductForm, OrderForm, StockForm, TransactionForm, InvoiceForm, InvoiceItemFormSet
from django.contrib.auth.models import User
from django.contrib import messages
from weasyprint import HTML
from django.template.loader import render_to_string
from django.db.models import Sum, F, ExpressionWrapper, FloatField

from django.utils.timezone import now
from django.utils.timezone import localdate
from geopy.distance import geodesic
from .models import Attendance

from user.models import Profile  # Import Profile model
from .utils import is_within_branch_location  # Ensure this function is imported

from .models import Sale
from .forms import SaleForm

from decimal import Decimal
import re
from .forms import ProductForm

from .models import Loan, Product
from .forms import LoanForm








@login_required(login_url='dashboard-login')
def index(request):
    orders = Order.objects.all()
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form':form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'index.html', context)


@login_required(login_url='dashboard-login')
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    
    context={
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'staff.html', context)


@login_required(login_url='dashboard-login')
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers': workers,
    }
    return render(request, 'staff_detail.html', context)


@login_required(login_url='dashboard-login')
def product(request):
    items = Product.objects.all() #Using ORM (Object relational mapping method)
    product_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
        

    if request.method =='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-product')
    else:
        form = ProductForm()     
                   
    context = {
        'items': items,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
        
        
    }
    return render(request, 'product.html', context)


@login_required(login_url='dashboard-login')
def product_delete(request, pk): #product delete
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'product_delete.html')


@login_required(login_url='dashboard-login')
def product_update(request, pk): #product update
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context={
        'form': form,
    }
    return render(request, 'product_update.html', context)




@login_required(login_url='dashboard-login')
def orders(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    product_count = Product.objects.all().count()
   

    context={
        'orders':orders,
        'workers_count': workers_count,
        'orders_count' : orders_count,
        'product_count' : product_count,   
    }
    return render(request, 'orders.html', context)



# 🔹 List all stock items
@login_required(login_url='dashboard-login')

def total_stock_summary(request):
    total_stocks = (
        Stock.objects.values('product__name', 'branch__name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('product__name', 'branch__name')
    )

    total_value = (
        Stock.objects.aggregate(total_worth=Sum(F('quantity') * F('product__price')))['total_worth'] or 0
    )

    return render(request, 'total_stock_summary.html', {
        'total_stocks': total_stocks,
        'total_value': total_value
    })



def branch_stock_summary(request):
    staff_profile = Profile.objects.filter(staff=request.user).first()
    
    if not staff_profile or not staff_profile.branch:
        return render(request, 'error.html', {'message': 'You are not assigned to a branch.'})

    branch = staff_profile.branch
    stocks = Stock.objects.filter(branch=branch)
    total_value = sum((stock.quantity or 0) * (stock.product.price or 0) for stock in stocks)
    
    return render(request, 'branch_stock_summary.html', {'branch': branch, 'total_value': total_value, 'stocks': stocks})


@login_required(login_url='dashboard-login')
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})


def stock_update(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()  # Directly save the updated stock
            messages.success(request, "Stock updated successfully!")
            return redirect('dashboard-stock_list')

    else:
        form = StockForm(instance=stock)

    return render(request, 'stock_form.html', {'form': form})



def stock_delete(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, "Stock deleted successfully!")
        return redirect('dashboard-stock_list')
    return render(request, 'stock_delete.html', {'stock': stock})


def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()  # Just save, let the model handle stock updates
            messages.success(request, f"Transaction {transaction.transaction_type} recorded successfully!")
            return redirect('dashboard-transaction_list')

    else:
        form = TransactionForm()

    return render(request, 'create_transaction.html', {'form': form})







def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')  # Show latest transactions first
    return render(request, 'transaction_list.html', {'transactions': transactions})



def create_invoice(request):
    if request.method == "POST":
        invoice_form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)

        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save()  # Create the invoice first
            items = formset.save(commit=False)

            for item in items:
                item.invoice = invoice  # Assign the invoice to each item
                item.save()

            formset.save_m2m()  # Save many-to-many relationships if any
            return redirect('dashboard-invoice_detail', invoice_id=invoice.id)

    else:
        invoice_form = InvoiceForm()
        formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.none())  # Empty formset

    return render(request, 'create_invoice.html', {'invoice_form': invoice_form, 'formset': formset})



def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'invoice_detail.html', {'invoice': invoice})


def generate_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    html_string = render_to_string('invoice_pdf.html', {'invoice': invoice})
    
    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{invoice.id}.pdf"'
    return response



@login_required
def clock_in_out(request):
    if request.method == "POST":
        latitude = request.POST.get("latitude", "").strip()
        longitude = request.POST.get("longitude", "").strip()

        if not latitude or not longitude:
            messages.error(request, "Location data is required to clock in/out.")
            return redirect("dashboard-attendance")

        try:
            user_lat = float(latitude)
            user_long = float(longitude)
        except ValueError:
            messages.error(request, "Invalid location data received.")
            return redirect("dashboard-attendance")

        staff = request.user
        staff_profile = getattr(staff, "profile", None)  # Get the user's profile

        if not staff_profile or not staff_profile.branch:
            messages.error(request, "No branch assigned!")
            return redirect("dashboard-attendance")

        branch = staff_profile.branch

        if not is_within_branch_location(user_lat, user_long, branch):
            messages.error(request, "You must be within the branch premises to clock in/out.")
            return redirect("dashboard-attendance")

        attendance, created = Attendance.objects.get_or_create(user=staff, branch=branch, clock_out__isnull=True)

        if created:
            attendance.clock_in = now()
            messages.success(request, "Clock-in successful!")
        else:
            attendance.clock_out = now()
            messages.success(request, "Clock-out successful!")

        attendance.save()
        return redirect("dashboard-attendance")

    return render(request, "attendance.html")


def is_within_branch_location(user_lat, user_long, branch):
    """Check if user is within the branch's location radius."""
    try:
        branch_location = (float(branch.latitude), float(branch.longitude))
        user_location = (float(user_lat), float(user_long))
        return geodesic(user_location, branch_location).km <= branch.radius
    except (ValueError, TypeError):
        return False


@login_required
def attendance_list(request):
    records = Attendance.objects.all().order_by("-date")
    return render(request, "attendance_list.html", {"records": records})


@login_required

def staff_daily_sales_report(request):
    """Generate a sales report for the logged-in staff."""
    staff = request.user
    today = localdate()

    # Filter sales for the logged-in staff on today's date
    sales = Sale.objects.filter(staff=staff, timestamp__date=today)

    # Calculate totals
    total_sales = sum(sale.total_price for sale in sales)
    total_discount = sum(sale.discount for sale in sales)

    context = {
        "sales": sales,
        "total_sales": total_sales,
        "total_discount": total_discount,
        "staff": staff,
        "date": today,
    }

    return render(request, "sales_report.html", context)


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.price = clean_price(request.POST.get("price", "0.00"))  # Apply cleaning manually if needed
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect("dashboard-index")
    else:
        form = ProductForm()
    
    return render(request, "index.html", {"form": form})


def clean_price(price_str):
    """ Remove currency symbols, commas, and convert to Decimal """
    from decimal import Decimal
    import re

    cleaned_price = re.sub(r"[^\d.]", "", str(price_str))  # Remove non-numeric characters except "."
    return Decimal(cleaned_price) if cleaned_price else Decimal("0.00")



def issue_loan(request):
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            
            if loan.product.quantity_in_stock < loan.quantity:
                messages.error(request, "Not enough stock available!")
                return redirect("dashboard-issue-loan")

            loan.product.quantity_in_stock -= loan.quantity  # Deduct from stock
            loan.product.save()
            loan.save()
            
            messages.success(request, "Loan issued successfully!")
            return redirect("dashboard-loan-list")
    else:
        form = LoanForm()

    return render(request, "issue_loan.html", {"form": form})

def loan_list(request):
    loans = Loan.objects.all()
    return render(request, "loan_list.html", {"loans": loans})

def return_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    
    if loan.is_returned:
        messages.info(request, "This loan has already been returned.")
    else:
        loan.mark_as_returned()
        messages.success(request, "Loan returned successfully!")

    return redirect("dashboard-loan-list")