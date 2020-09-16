from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('stock', views.stock, name='stock'),
    path('sales', views.sale, name='sales'),
    path('category', views.category, name='category'),

    path('worker', views.worker, name='worker'),
    path('refund', views.refund, name='refund'),
    path('sales-register', views.saleRegister, name='sales-register'),
   
    path('update-stock/<p_id>', views.update_stock, name='update-stock'),
    path('update-worker/<p_id>', views.update_worker, name='update-worker'),
    path('delete-stock/<p_id>', views.delete_stock, name='delete-stock'),
    path('delete-worker/<p_id>', views.delete_worker, name='delete-worker'),

    path('logout',views.logout_view, name='logout')
]
