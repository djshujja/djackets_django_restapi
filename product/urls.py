from django.urls import path, include

from product import views

urlpatterns = [
	path('orders/', views.AllOrders.as_view()),
	path('latest-products/', views.LatestProductsList.as_view()),
	path('products/search/', views.search),
	path('products/inc-price/', views.inc_price),
	path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
	path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),

]