from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from django.db import transaction

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, 
        related_name='sub_categories', null=True, blank=True
    )
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    image = models.ImageField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    sold = models.PositiveIntegerField(default=0)  
    stock = models.PositiveIntegerField(default=0) 
    sale_percent = models.PositiveIntegerField(default=0)

    @property
    def final_price(self):
        """Tính toán giá cuối cùng sau giảm giá"""
        if self.sale_percent > 0:
            return self.price * (100 - self.sale_percent) / 100
        return self.price

    @property
    def ImageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Chờ xác nhận'),
        ('Processing', 'Đang xử lý'),
        ('Shipped', 'Đang giao hàng'),
        ('Delivered', 'Đã giao hàng'),
        ('Cancelled', 'Đã hủy'),
    )
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False) 
    is_processed = models.BooleanField(default=False) 
    session_key = models.CharField(max_length=200, null=True, blank=True, db_index=True)
    transaction_id = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0) 
    payment_method = models.CharField(max_length=100, default='COD')

    def __str__(self):
        return f"Order {self.id}"

    @property
    def get_cart_total(self):
        """Tính tổng tiền của tất cả các mặt hàng trong giỏ"""
        orderitems = self.items.all() 
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        """Tính tổng số lượng sản phẩm (con số hiển thị trên icon giỏ hàng)"""
        orderitems = self.items.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def cart_total_vnd(self):
       
        return self.get_cart_total

class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=0)
    
    price_at_order = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.price_at_order * self.quantity
    
    @property
    def total_vnd(self):
        return self.get_total

class ShoppingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True) 
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=255)


@receiver(post_save, sender=Order)
def update_stock_and_sold(sender, instance, created, **kwargs):
    """
    Sử dụng F() expression để tránh Race Condition (xung đột dữ liệu).
    Sử dụng transaction.atomic để đảm bảo dữ liệu nhất quán.
    """
    if instance.complete and not instance.is_processed:
        with transaction.atomic():
            order_items = instance.items.all().select_related('product')
            for item in order_items:
                if item.product:
                   
                    Product.objects.filter(id=item.product.id).update(
                        sold=F('sold') + item.quantity,
                        stock=F('stock') - item.quantity
                    )
            
            Order.objects.filter(id=instance.id).update(is_processed=True)