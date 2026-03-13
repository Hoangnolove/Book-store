from .models import Category

def global_context(request):
    categories = Category.objects.filter(sub_category__isnull=True).prefetch_related('sub_categories')
    
    return {
        'categories': categories
    }