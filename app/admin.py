from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('indented_name',)
    ordering = ('sub_category__id',)

    def indented_name(self, obj):
        level = 0
        parent = obj.sub_category
        while parent:
            level += 1
            parent = parent.sub_category
        return "— " * level + obj.name

    indented_name.short_description = "Category"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShoppingAddress)



