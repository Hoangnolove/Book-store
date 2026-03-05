from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    sub_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='sub_categories',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name
class CreateUserForm(UserCreationForm):
     class Meta:
          model = User
          fields = ['username','email','first_name','last_name','password1','password2']


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    image = models.ImageField(null=True,blank=True)
    detail = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
              url = self.image.url
        except:
            url = ''
        return url
    @property
    def price_vnd(self):
        return f"{int(self.price):,}".replace(",", ".")
class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())

    @property
    def get_cart_total(self):
        return sum(item.get_total for item in self.orderitem_set.all())

    @property
    def cart_total_vnd(self):
        if self.get_cart_total == 0:
            return "0 đ"
        return f"{self.get_cart_total:,.0f}".replace(",", ".") + " đ"


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product and self.product.price:
            return self.product.price * self.quantity
        return 0

    @property
    def total_vnd(self):
        return f"{self.get_total:,.0f}".replace(",", ".") + " đ"
class ShoppingAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=255)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.mobile}"
