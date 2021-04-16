# from django.shortcuts import render
from django.db.models import Q
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer
from .models import Product, Category, Order



class LatestProductsList(APIView):
	def get(self, request, format=None):
		products = Product.objects.all()[0:4]
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data)


class ProductDetail(APIView):
	def get_object(self, category_slug, product_slug):
		try:
			return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
		except Product.DoesNotExist:
			raise Http404

	def get(self, request, category_slug, product_slug, format=None):
		product = self.get_object(category_slug, product_slug)
		serializer = ProductSerializer(product)
		return Response(serializer.data)


class CategoryDetail(APIView):
	def get_object(self, category_slug):
		try:
			return Category.objects.get(slug=category_slug)
		except Category.DoesNotExist:
			raise Http404

	def get(self, request, category_slug, format=None):
		category = self.get_object(category_slug)
		serializer = CategorySerializer(category)
		return Response(serializer.data)




class AllOrders(APIView):
	def get_object(self):
		try:
			return Order.objects.all()
		except Order.DoesNotExist:
			raise Http404
	def get(self, request, format=None):
		orders = self.get_object()
		serializer = OrderSerializer(orders, many=True)
		return Response(serializer.data)



@api_view(["POST"])
def search(request):
	query = request.data.get('query')
	if query:
		products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) )
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data)
	else:
		return Response({"products": []}) 


@api_view(["POST"])
def inc_price(request):
	product_slug = request.data.get('product_slug')
	db_product = Product.objects.get(slug=product_slug)
	db_product.price = 0.00
	db_product.save()
	serializer = ProductSerializer(db_product)
	return Response(serializer.data)


@api_view(['POST'])
def add_category(request):
	name = request.data.get('name')
	slug = request.data.get('slug')
	price = request.data.get('price')
	new_category = Category.objects.create(
		name = name,
		slug = slug,
		)
	new_category.save()
	return JsonResponse({
		"message":"succesfully created!"
		})
	# serializer = CategorySerializer(new_category)
	# return Response(serializer.data)

@api_view(['GET'])
def all_categories(request):
	categories = Category.objects.all()
	serializer = CategorySerializer(categories,many=True)
	return Response(serializer.data)


# @api_view(["POST"])
# def place_order(request):

