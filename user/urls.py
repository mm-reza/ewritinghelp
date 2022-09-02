"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from.import views



urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.password_update, name='password_update'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orders_product/', views.user_order_product, name='user_order_product'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
    path('comments/', views.user_comments, name='user_comments'),
    path('replys/', views.user_replys, name='user_replys'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),
    path('deletefiles/<int:id>', views.user_deletefiles, name='user_deletefiles'),
    path('reply/<int:id>', views.reply, name='reply'),
    path('files', views.files, name='files'),
]
