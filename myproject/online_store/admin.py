from django.contrib import admin
from .models import Client, Goods, Order


# функция для изменения данных
@admin.action(description="Сбросить количество в ноль")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)


# Колонки отображаемые в админ. панеле Django
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'product_added_date']  # список отображаемых продуктов
    ordering = ['price', '-quantity']  # сортировка
    list_filter = ['price', 'product_added_date', 'quantity']  # фильтрование
    search_fields = ['price']
    search_help_text = "Поиск по цене (price) "
    actions = [reset_quantity]

    """Отдельный продукт"""
    fields = ['name', 'price', 'quantity', 'product_added_date']
    readonly_fields = ['product_added_date']


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'date_reg')





class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'total_price', 'date_order']


admin.site.register(Client, ClientAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Order, OrderAdmin)
