from django.shortcuts import render
from invoice.models import UserDetail, Invoice
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q 

def signUp(request):
  if request.session.has_key('username'):
    username = request.session['username']
    return redirect(welcome, username)
  elif request.method=='POST':
    try:
      user = UserDetail.objects.get(username=request.POST['username'])
    except:
      user = None
    try:
      user1 = UserDetail.objects.get(email_id=request.POST['email_id'])
    except:
      user1 = None
    if user is not None and user1 is not None:
      messages.info(request, "Email ID is already exists")
    else:
      new_user = UserDetail()
      new_user.username = request.POST['username']
      new_user.email_id = request.POST['email_id']
      new_user.password = request.POST['password']
      new_user.user_type = request.POST['user_type']
      new_user.save()
  return render(request, 'signup.html', {})


def login(request):
  if request.session.has_key('username'):
    username = request.session['username']
    return redirect(welcome, username)
  elif request.method=="POST":
    email_id = request.POST['email_id']
    password = request.POST['password']
    try:
      user = UserDetail.objects.get(email_id=email_id)
    except:
      user = None
    if user is None:
      messages.info(request, "Email ID and Password is Incorrect")
      return redirect(login)
    else:
      if user.email_id==email_id and user.password==password:
        request.session['username'] = user.username
        return redirect(welcome, user.username)
      else:
        messages.info(request, "Password is Incorrect")
        return redirect(login)
  return render(request, 'login.html', {})


def logout(request):
  if request.session.has_key('username'):
    del request.session['username']
    return redirect(login)


def welcome(request, username):
  if username == request.session['username']:
    user = UserDetail.objects.get(username=username)
    if(user.user_type=='ADMIN'):
      invoices = Invoice.objects.filter(status='PENDING')
    else:
      invoices = Invoice.objects.filter(status='PENDING', user_id=user)
    return render(request, 'welcome.html', {'username':username, 'user_type':user.user_type, 'invoices':invoices})
  else:
    return render(request, 'welcome.html', {'username': 'None'})

def createInvoice(request, username):
  if username == request.session['username']:
    user = UserDetail.objects.get(username=username)
    if user.user_type=='NORMAL':
      if request.method=='POST':
        invoice = Invoice()
        invoice.name = request.POST['invoice_name']
        invoice.date = request.POST['date']
        invoice.amount = request.POST['amount']
        invoice.image = request.POST['invoice_image']
        invoice.user = user
        invoice.save()
      return render(request, 'create_invoice.html', {'username':username})
  return render(request, 'create_invoice.html', {'username':'None'})

def viewInvoice(request, username): 
  if username == request.session['username']:
    login_user = UserDetail.objects.get(username=username)
    total_amount = 0
    if(login_user.user_type == 'ADMIN'):
      invoices = Invoice.objects.all()
      all_invoices = list()
      for invoice in invoices:
        user_invoice = dict()
        user = UserDetail.objects.get(pk=invoice.user_id)
        user_invoice['invoice_id'] = invoice.id
        user_invoice['username'] = user.username
        user_invoice['name'] = invoice.name
        user_invoice['date'] = invoice.date
        user_invoice['amount'] = invoice.amount
        user_invoice['status'] = invoice.status
        total_amount+=invoice.amount
        all_invoices.append(user_invoice)
    else:
      all_invoices = Invoice.objects.filter(user_id=login_user)
      for invoice in all_invoices:
        total_amount+=invoice.amount
    return render(request, 'view_invoices.html', {'invoices':all_invoices, 'total_amount' : total_amount, 'username' : username, 'user_type': login_user.user_type, 'total_invoices' : len(all_invoices)})
  return render(request, 'view_invoices.html', {'username':'None'})

def filterInvoice(request, username):
  if username == request.session['username']:
    login_user = UserDetail.objects.get(username=username)
    total_amount = 0
    if(login_user.user_type == 'ADMIN'):
      invoices = Invoice.objects.filter(date__range=[request.POST['startdate'], request.POST['enddate']])
      all_invoices = list()
      for invoice in invoices:
        user_invoice = dict()
        user = UserDetail.objects.get(pk=invoice.user_id)
        user_invoice['username'] = user.username
        user_invoice['name'] = invoice.name
        user_invoice['date'] = invoice.date
        user_invoice['amount'] = invoice.amount
        total_amount+=invoice.amount
        all_invoices.append(user_invoice)
      return render(request, 'view_invoices.html', {'invoices':all_invoices, 'total_amount' : total_amount, 'username' : username, 'user_type': login_user.user_type, 'total_invoices' : len(all_invoices)})
    else:
      invoices = Invoice.objects.filter(date__range=[request.POST['startdate'], request.POST['enddate']])
      for invoice in invoices:
        total_amount+=invoice.amount
      return render(request, 'view_invoices.html', {'invoices':invoices, 'total_amount' : total_amount, 'username' : username, 'user_type': login_user.user_type, 'total_invoices' : len(invoices)})
  return render(request, 'view_invoices.html', {'username':'None'})

def deleteInvoice(request, username, id):
  if username == request.session['username']:
    user = UserDetail.objects.get(username=username)
    try:
      if(user.user_type!='ADMIN'):
        invoice = Invoice.objects.get(user_id=user, id=id, status="PENDING")
      else:
        invoice = Invoice.objects.get(id=id)
      invoice.delete()
      if(user.user_type=='ADMIN'):
        return redirect(viewInvoice, username)
      return redirect(welcome, username)
    except Exception as e:
      return render(request, 'welcome.html', {'username': 'None'})
  else:
    return render(request, 'welcome.html', {'username': 'None'})

def editInvoice(request, username, id):
  if username == request.session['username']:
    user = UserDetail.objects.get(username=username)
    try:
      if(user.user_type!='ADMIN'):
        invoice = Invoice.objects.get(user_id=user, id=id, status="PENDING")
      else:
        invoice = Invoice.objects.get(id=id)
      return render(request, 'update_invoice.html', {'invoice':invoice, 'username':username, 'id':id})
    except Exception as e:
      return render(request, 'welcome.html', {'username': 'None'})
  else:
    return render(request, 'welcome.html', {'username': 'None'})

def updateInvoice(request, username, id):
  if username == request.session['username']:
    user = UserDetail.objects.get(username=username)
    try:
      if(user.user_type!='ADMIN'):
        #invoice = Invoice.objects.get(user_id=user, id=id, status="PENDING")
        Invoice.objects.filter(id=id, user_id=user, status="PENDING").update(name = request.POST.get('invoice_name'), date = request.POST.get('date'), amount = request.POST.get('amount'), image = request.POST.get('invoice_image'))
      else:
        Invoice.objects.filter(~Q(status="PENDING"), id=id).update(name = request.POST.get('invoice_name'), date = request.POST.get('date'), amount = request.POST.get('amount'), image = request.POST.get('invoice_image'))
      if(user.user_type=='ADMIN'):
        return redirect(viewInvoice, username)
      return redirect(welcome, username)
    except Exception as e:
      return render(request, 'welcome.html', {'username': 'None'})
  else:
    return render(request, 'welcome.html', {'username': 'None'})


def updateStatus(request, username, id):
  if username == request.session['username']:
    try:
      Invoice.objects.filter(id=id).update(status=request.POST['status'])
      return redirect(welcome, username)
    except Exception as e:
      return render(request, 'welcome.html', {'username': 'None'})
  else:
    return render(request, 'welcome.html', {'username': 'None'})


"""
def pendingInvoices(request, username):
  user = UserDetail.objects.get(username=username)
  if(user.user_type=='ADMIN'):
    invoices = Invoice.objects.filter(status='PENDING')
  else:
    invoices = Invoice.objects.filter(status='PENDING', user_id=user)
  return render(request, 'view_invoices.html', {'invoices':invoices, 'total_amount':0})"""
