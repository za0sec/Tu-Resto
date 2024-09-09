from django.db import models


class Order(models.Model):
    """ Customer Order """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField('products.Product', through='OrderItem')
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    discount = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    commentary = models.CharField(max_length=255, null=True, blank=True)
    
    def get_total(self):
        return sum([item.get_total() for item in self.order_items.all()])


class OrderItem(models.Model):
    """ Order Item """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    extras = models.ManyToManyField('products.ProductExtra')
    commentary = models.CharField(max_length=255, null=True, blank=True)

    def get_total(self):
        total = self.product.price * self.quantity
        for extra in self.extras.all():
            total += extra.price * self.quantity
        return total

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name} x {self.quantity}"


class TableOrder(Order):
    """ Table Order """
    table = models.ForeignKey('restaurant.Table', on_delete=models.CASCADE)

    def __str__(self):
        return f"Table {self.table.number} Order {self.order.id}"


class DeliveryOrder(Order):
    """ Delivery Order """
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Delivery Order {self.id} at {self.address}"


class TakeAwayOrder(Order):
    """ Take Away Order """
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    cashier = models.ForeignKey('users.Cashier', on_delete=models.CASCADE)
    ready = models.BooleanField(default=False)

    def __str__(self):
        return f"Take Away Order {self.id}"