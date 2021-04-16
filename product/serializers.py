from rest_framework import serializers
from .models import Category, Product, Order, OrderProduct

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = (
			"id",
			"name",
			"get_absolute_url",
			"description",
			"price",
			"get_image",
			"get_thumbnail"
			)


class OrderProductSerializer(serializers.ModelSerializer):
	product = ProductSerializer(many=False)
	class Meta:
		model = OrderProduct
		fields = (
			"id",
			"product",
			"qty",
			)


class OrderSerializer(serializers.ModelSerializer):
	products = OrderProductSerializer(many=True)
	class Meta:
		model = Order
		fields = (
			"id",
			"order_id",
			"status",
			"products"
			)	


class CategorySerializer(serializers.ModelSerializer):
	products = ProductSerializer(many=True)
	class Meta:
		model = Category
		fields = (
			"id",
			"name",
			"get_absolute_url",
			"products",
			)

