from django.contrib import admin
from .models import *


class ShoppingAddressInline(admin.StackedInline):
    model = ShoppingAddress
    extra = 0
    can_delete = False
    readonly_fields = ('name', 'mobile', 'city', 'address')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'customer', 'get_cart_total_display', 'status', 'complete', 'date_order')
    list_editable = ('status', 'complete') 
    list_filter = ('status', 'complete', 'date_order')
    inlines = [ShoppingAddressInline]
    search_fields = ('id', 'customer__username', 'transaction_id')

    def get_cart_total_display(self, obj):
        
        return f"{obj.total_price:,.0f} đ" if hasattr(obj, 'total_price') else "0 đ"
    get_cart_total_display.short_description = 'Tổng tiền'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('indented_name', 'slug')
    prepopulated_fields = {'slug': ('name',)} 

    def indented_name(self, obj):
        level = 0
        parent = obj.sub_category
        while parent:
            level += 1
            parent = parent.sub_category
        return "— " * level + str(obj.name)
    indented_name.short_description = "Tên danh mục"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'price', 'sale_percent', 'discount_price_display','stock', 'sold', 'check_sale_status')
    list_editable = ('sale_percent', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('category',)

    def discount_price_display(self, obj):
        return f"{int(obj.final_price):,}".replace(",", ".") + " đ"
    discount_price_display.short_description = 'Giá sau giảm'

    
    def check_sale_status(self, obj):
        return obj.sale_percent > 0
    check_sale_status.boolean = True 
    check_sale_status.short_description = 'Đang giảm giá'


admin.site.register(OrderItem)
admin.site.register(ShoppingAddress)