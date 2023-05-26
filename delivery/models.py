from django.contrib.auth.models import User
from django.db import models
from geolocation_fields.models import fields


class FoodCategory(models.Model):
    name = models.CharField(max_length=75, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    geo = fields.PointField()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'establishment_category'


class Establishments(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255 ,null=True)
    type = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
    photo = models.ImageField(default='images.jpeg', blank=True, null=True)
    logo = models.ImageField(default='logo.jpg', blank=True, null=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    bio = models.TextField()
    photo = models.ImageField(blank=True)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE,null=True)
    establishment = models.ForeignKey(Establishments, on_delete=models.CASCADE ,null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.IntegerField()
    total_price = models.IntegerField()
    establishment = models.ForeignKey(Establishments, on_delete=models.CASCADE, null=True)
    readiness = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_foods')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return f"{self.food} x{self.amount} - {self.order.customer.user.username}"


class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.food.name)

    def total_price(self):
        return self.food.price * self.quantity


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.full_name
