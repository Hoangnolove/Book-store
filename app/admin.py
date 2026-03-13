from django.contrib import admin
from .models import *


class ShoppingAddressInline(admin.StackedInline):
    model = ShoppingAddress
    extra = 0
    can_delete = False
    readonly_fields = ('name', 'mobile', 'city', 'address')

class OrderAdmin(admin.ModelAdmin):
   
    list_display = ('id', 'customer', 'get_cart_total_display', 'status', 'payment_method', 'complete', 'date_order')
    
    
    list_editable = ('status', 'complete') 
    
    
    list_filter = ('status', 'complete', 'date_order')
    
    
    inlines = [ShoppingAddressInline]
    search_fields = ('id', 'customer__username', 'transaction_id')

    def get_cart_total_display(self, obj):
        return obj.cart_total_vnd 
    get_cart_total_display.short_description = 'Tổng tiền'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('indented_name',)
    def indented_name(self, obj):
        level = 0
        parent = obj.sub_category
        while parent:
            level += 1
            parent = parent.sub_category
        return "— " * level + obj.name
    indented_name.short_description = "Category"


admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'price', 'discount_price', 'sold', 'is_on_sale')
    
    list_editable = ('discount_price',)
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem)
admin.site.register(ShoppingAddress)