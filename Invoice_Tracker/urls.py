"""Invoice_Tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from invoice import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signUp),
    path('login/', views.login),
    path('logout/', views.logout),
    path('invoices/<username>', views.welcome),
    path('invoices/<username>/create-new', views.createInvoice),
    path('invoices/<username>/all-invoices', views.viewInvoice),
    path('invoices/<username>/filter', views.filterInvoice),
    path('invoices/<username>/delete/<id>', views.deleteInvoice),
    path('invoices/<username>/edit/<id>', views.editInvoice),
    path('invoices/<username>/update/<id>', views.updateInvoice),
    path('invoices/<username>/updateStatus/<id>', views.updateStatus, name="updateStatus"),
    path('invoices/<username>/filterInvoice/', views.filterInvoice, name="filterInvoice"),
]
