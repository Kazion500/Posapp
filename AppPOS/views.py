from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import *
from .models import *

@login_required(redirect_field_name='login')
def dashboard(request):

   if not request.user.is_superuser:
      return redirect('sales')

   # DB Queries
   stocks = Stock.objects.all().order_by('-create_dated')
   workers = SalesPerson.objects.all().order_by('id').exclude(user__is_superuser=True)

   # Table Pagination
   paginator = Paginator(stocks,3,orphans=1)
   paginator1 = Paginator(workers,3,orphans=1)
   page_number1 = request.GET.get('stocks')
   page_number = request.GET.get('workers')
   page_obj = paginator.get_page(page_number1)
   page_obj1 = paginator1.get_page(page_number)

   # Solves the error DoseNotExist 
   try:
      lastest_sale = Sale.objects.latest('transaction_date')
   except:
      lastest_sale = 'Waiting for update'
   try:
      lastest_stock = Stock.objects.latest('create_dated')
   except:
      lastest_stock = 'Waiting for update'
   
   context = {
      "saleTotal": Sale.objects.aggregate(sum=Sum('total_price'))['sum'],
      "StocksTotal": Stock.objects.aggregate(count=Count('create_dated'))['count'],
      "salesPerson": workers.count(),
      
      "transDate": lastest_sale,
      "latestStockAdd": lastest_stock, 

      'stocks': page_obj,
      'workers': page_obj1,
   }
   return render(request, 'AppPOS/dashboard.html', context)


def index(request):

   if request.user.is_authenticated and request.user.is_staff:
      return redirect('dashboard')
   else:

      if request.method == 'POST':
         form = LoginUserForm(request.POST)

         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(request, username=username, password=password)

         if user is not None:
            login(request, user)
            
            return redirect('dashboard')

      else:
         form = LoginUserForm()

   context = {
      'form':form
   }
   return render(request, 'AppPOS/index.html',context)

@login_required(redirect_field_name='login')
def stock(request):

   stock = Stock.objects.all().order_by('-create_dated')
   category = Category.objects.all()

   # Stock pagination
   paginator = Paginator(stock,5,orphans=1)
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)

   if request.method == "POST":
      form = StockForm(request.POST,)
      form_category = CatgoryForm(request.POST,)

      """ 
      Validation checks to ensure that the right 
      information has been posted to the database
      """

      if form.is_valid():
         form.save()
         messages.success(request,'Product Registered Successfully')
         return redirect('stock')
         
      if form_category.is_valid():
         form_category.save()
         messages.success(request,'Catergory Registered Successfully')
         return redirect('stock')

   else:

      form = StockForm()
      form_category = CatgoryForm()

   context = {

      'catgoryID': category,
      'stock': page_obj,
      'form': form,
      'form_category': form_category
   }
   return render(request, 'AppPOS/stock.html', context)


@login_required(redirect_field_name='login')
def category(request):
   return render(request, 'AppPOS/category.html')


@login_required(redirect_field_name='login')
def sale(request):
   sold = []
   if request.user.is_superuser:
      sold += Sale.objects.all()
   sold += Sale.objects.filter(user__user__username=request.user).order_by('-transaction_date')
   paginator = Paginator(sold,5,orphans=1)
   page_number = request.GET.get('page')
   page_ojb = paginator.get_page(page_number)
   

   context = {
      'sold': page_ojb,
   }
   return render(request, 'AppPOS/sale.html', context)



@login_required(redirect_field_name='login')
def refund(request):

   refunds = Refund.objects.all()
   if request.method == 'POST':
      form = RefundForm(request.POST)
      product_id = form.data.get('product')
      product_qty = int(form.data.get('quantity'))

      stock = Stock.objects.get(product_id=product_id)
      sale = Sale.objects.get(product__product_id=product_id)
      if form.is_valid():
         form.save(commit=False)
         p_qty = stock.quantity + product_qty
         stock.quantity = p_qty
         stock.save()
         form.save()
         
   else:
      form = RefundForm()

   context = {
      'refunds':refunds,
      'form':form,
   }
   return render(request, 'AppPOS/refund.html', context)


@login_required(redirect_field_name='login')
def saleRegister(request):

   if not request.user.is_staff and request.user.is_superuser:
      return redirect('index')
   

   stock_cat = Category.objects.all()
   sold = Sale.objects.all()
   stocksDetail = Stock.objects.all()
   
   if request.method == "POST":
      form = SaleRegisterForm(request.POST)

      try:
         sale_qty = int(form.data['quantity'])
         sale_pid = form.data['product']

         if sale_qty != '' and sale_pid != '':
               
            stockDetail = Stock.objects.get(pk=sale_pid)
            stock_qty = stockDetail.quantity
            if sale_qty > stock_qty:
               messages.info(request,f'Cant process sale of {stockDetail.product_name} Only {stock_qty} remaining')
               
            else:
               if form.is_valid():
                  stock_qty -= sale_qty
                  stockDetail.quantity = stock_qty
                  stockDetail.save()
                  new_sale = form.save(commit=False)
                  new_sale.user = request.user.salesperson
                  new_sale.save() 
                  messages.success(request,f'Sale Processed Successfully!!')

                  return redirect('sales-register') 
                  
      except:
         sale_qty = None
         sale_pid = None
         stockDetail = None
         return redirect('sales-register')

   else:
      form = SaleRegisterForm()

   sale_StockName = request.GET.get('StockName')

   # reponding to ajax request

   if request.is_ajax():
         for stk in stocksDetail:
            if sale_StockName == stk.product_name:
                  # returns a json-response to frontend
                  return JsonResponse({
                     'product_id': stk.product_id,
                     'product_name': stk.product_name,
                     'product_price': stk.product_price,
                     'category_id': stk.category_id,
                  })
                  
 
   context = {
         'stock_cat': stock_cat,
         'sold': sold,
         'stockDetail': stocksDetail,
         'form_sales': form,
      }
   return render(request, 'AppPOS/sales-register.html', context)


@login_required(redirect_field_name='login')
def worker(request):
   workers = SalesPerson.objects.all().order_by('id').exclude(user__is_superuser=True)

   # Table Pagination
   paginator = Paginator(workers,5,orphans=1)
   page_number = request.GET.get('workers')
   page_obj = paginator.get_page(page_number)

   if request.method == 'POST':
      form_user = SignUpUserForm(request.POST)

      if form_user.is_valid():
         # saving an instance of the worker
         user = form_user.save()
         user.refresh_from_db()
         user.salesperson.nrc = form_user.cleaned_data.get('nrc')
         user.salesperson.phone = form_user.cleaned_data.get('phone')
         user.salesperson.location = form_user.cleaned_data.get('location')
         user.salesperson.gender = form_user.cleaned_data.get('gender')
         user.is_staff = True
         user.save()
         raw_password = form_user.cleaned_data.get('password1')
         username = form_user.cleaned_data.get('username')
         user = authenticate(username=username,password=raw_password)

         messages.success(request,'User Registered Successfully')
         # login(request,user)
         
         return redirect('worker')

   else:
      form_user = SignUpUserForm()


   context = {
      'workers':page_obj,
      'form_user':form_user,
   }
   return render(request, 'AppPOS/worker.html',context)


# update view (Stock)
@login_required(redirect_field_name='login')
def update_stock(request, p_id):
   stock_data = Stock.objects.get(product_id=p_id)
   if request.method == 'POST':
      stock_form_update = StockForm(request.POST, instance=stock_data)

      if stock_form_update.is_valid():
         new_update = stock_form_update.save(commit=False)
         new_update.save()
         return redirect('stock')

   stock_form_update = StockForm(instance=stock_data)
   context = {
      'stock_form_update': stock_form_update,
   }
   return render(request, 'AppPOS/update.html', context)

# update view (Worker)
@login_required(redirect_field_name='login')
def update_worker(request, p_id):
   worker_data = SalesPerson.objects.get(pk=p_id)
   if request.method == 'POST':
      worker_form_update = WorkersForm(request.POST, instance=worker_data)

      if worker_form_update.is_valid():
         worker_form_update.save()
         return redirect('worker')

   worker_form_update = WorkersForm(instance=worker_data)
   
   context = {
      'worker_form_update': worker_form_update,
   }
   return render(request, 'AppPOS/update.html', context)

# delete view

@login_required(redirect_field_name='login')
def delete_stock(request, p_id):
 
   stock_data = Stock.objects.get(pk=p_id)
   stock_data.delete()
   return redirect('stock')


@login_required(redirect_field_name='login')
def delete_worker(request, p_id):
 
   worker_data = User.objects.get(pk=p_id)
   worker_data.delete()
   return redirect('stock')


@login_required(redirect_field_name='login')
def logout_view(request):
   logout(request)
   return redirect('index')