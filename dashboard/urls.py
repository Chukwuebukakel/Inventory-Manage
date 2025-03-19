from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin




urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/detail/<int:pk>/', views.staff_detail, name='dashboard-staff_detail'),
    path('product/', views.product, name='dashboard-product'),
    path('product/delete/<int:pk>/', views.product_delete, name='dashboard-product_delete'),
    path('product/update/<int:pk>/', views.product_update, name='dashboard-product_update'),
    path('orders/', views.orders, name='dashboard-orders'),

    path('stocks/', views.stock_list, name='dashboard-stock_list'),
    path("branch-stock-summary/", views.branch_stock_summary, name="dashboard-branch-stock-summary"),
    path('branches/stock-summary/', views.total_stock_summary, name='dashboard-total_stock_summary'),
    

    path('stock/update/<int:stock_id>/', views.stock_update, name='dashboard-stock_update'),
    path('stock/delete/<int:stock_id>/', views.stock_delete, name='dashboard-stock_delete'),

    
    path('transactions/', views.transaction_list, name='dashboard-transaction_list'),

    path('transactions/new/', views.create_transaction, name='dashboard-create_transaction'),

    path('invoice/new/', views.create_invoice, name='dashboard-create_invoice'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='dashboard-invoice_detail'),
    path('invoice/<int:invoice_id>/pdf/', views.generate_invoice_pdf, name='dashboard-generate_invoice_pdf'),
    
    path("attendance/", views.clock_in_out, name="dashboard-attendance"),
    path("attendance-list/", views.attendance_list, name="dashboard-attendance_list"),

   
    path('sales/daily-report/', views.staff_daily_sales_report, name='dashboard-staff-daily-sales'),

    path("issue-loan/", views.issue_loan, name="dashboard-issue-loan"),
    path("return-loan/<int:loan_id>/", views.return_loan, name="dashboard-return-loan"),
    path("loans/", views.loan_list, name="dashboard-loan-list"),

]


if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)