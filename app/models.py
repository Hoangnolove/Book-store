from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, 
        related_name='sub_categories', null=True, blank=True
    )
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    image = models.ImageField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    sold = models.PositiveIntegerField(default=0)  
    discount_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True) 

    @property
    def is_on_sale(self):
        return self.discount_price is not None and self.discount_price < self.price
    
    @property
    def final_price(self):
        return self.discount_price if self.is_on_sale else self.price

    @property
    def price_vnd(self):
        return f"{int(self.price):,}".replace(",", ".")

    @property
    def discount_price_vnd(self):
        if self.discount_price:
            return f"{int(self.discount_price):,}".replace(",", ".")
        return ""

    @property
    def ImageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return self.name
    
    @property
    def sale_percent(self):
        if self.is_on_sale:
            percent = ((self.price - self.discount_price) / self.price) * 100
            return int(percent)
        return 0

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    complete = models.BooleanField(default=False) 
    is_processed = models.BooleanField(default=False) 
    transaction_id = models.CharField(max_length=200, null=True)
    
    STATUS_CHOICES = (
        ('Pending', 'Chờ xác nhận'),
        ('Processing', 'Đang xử lý'),
        ('Shipped', 'Đang giao hàng'),
        ('Delivered', 'Đã giao hàng'),
        ('Cancelled', 'Đã hủy'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=100, default='COD')
    note = models.TextField(null=True, blank=True)

    @property
    def get_cart_total(self):
        return sum(item.get_total for item in self.orderitem_set.all())

    @property
    def cart_total_vnd(self):
        return f"{self.get_cart_total:,.0f}".replace(",", ".") + " đ"
    

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product:
            return self.product.final_price * self.quantity
        return 0
    
    @property
    def total_vnd(self):
        return f"{int(self.get_total):,}".replace(",", ".") + " đ"

class ShoppingAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Order)
def update_stock_and_sold(sender, instance, created, **kwargs):
    
    if instance.complete and not instance.is_processed:
        order_items = instance.orderitem_set.all()
        for item in order_items:
            product = item.product
            if product:
                product.sold += item.quantity 
                product.save()
        
        
        Order.objects.filter(id=instance.id).update(is_processed=True)