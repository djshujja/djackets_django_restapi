from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
import secrets

class Category(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return f'/{self.slug}/'

class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	description = models.TextField(blank=True, null=True)
	stock = models.IntegerField(default=0)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	image = models.ImageField(upload_to="uploads/", blank=True, null=True)
	thumbnail = models.ImageField(upload_to="uploads/", blank=True, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-date_added',)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return f'/{self.category.slug}/{self.slug}/'

	def get_image(self):
		if self.image:
			return f'http://localhost:8000' + self.image.url
		else:
			return ''

	def get_thumbnail(self):
		if self.thumbnail:
			return f'http://localhost:8000' + self.thumbnail.url
		else:
			if self.image:
				self.thumbnail = self.make_thumbnail(self.image)
				self.save()
				return f'http://localhost:8000' + self.thumbnail.url
			else:
				return ''

	def make_thumbnail(self, image, size=(300,200)):
		img = Image.open(image)
		img.convert('RGB')
		img.thumbnail(size)
		thumb_io = BytesIO()
		img.save(thumb_io, 'JPEG', quality=85)
		thumbnail = File(thumb_io, name=image.name)
		return thumbnail

class OrderProduct(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, primary_key=False)
	qty = models.IntegerField(default=1)

class Order(models.Model):
	order_id = models.CharField(default=secrets.token_hex(5), max_length=25)
	# user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
	bill = models.DecimalField(max_digits=6, decimal_places=2)
	status = models.BooleanField(default=False)
	products = models.ManyToManyField(OrderProduct,null=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-date',)

	def __str__(self):
		return self.order_id



















