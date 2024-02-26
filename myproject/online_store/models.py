from django.db import models

from datetime import datetime


class Goods(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()  # описание товара
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()  # количество товара
    image = models.ImageField(upload_to='goods/')
    product_added_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'name product: {self.name}, description: {self.description}, price: {self.price}, ' \
               f'quantity: {self.quantity}, product_added_date: {self.product_added_date}'


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    date_reg = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Username: {self.name}, email: {self.email}, phone: {self.phone}, ' \
               f'address: {self.address}, date_reg: {self.date_reg}'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)    # клиент который сделал заказ
    product = models.ManyToManyField(Goods)                         # заказанный продукт
    total_price = models.DecimalField(max_digits=8, decimal_places=2)  # общая сумма заказа
    date_order = models.DateTimeField(auto_now_add=True)                # дата оформления заказа




    def __str__(self):
        return f'{self.id}, client: {self.client.name}, product: {self.product.all()}, total_price: {self.total_price}, ' \
               f'date_ordered: {self.date_order}'


class Image(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to='images/', null=True, max_length=255)

    def __repr__(self):
        return 'Image(%s, %s)' % (self.title, self.image)

    def __str__(self):
        return self.title