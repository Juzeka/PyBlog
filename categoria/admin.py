from django.contrib import admin
from .models import Categoria
# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id','nome_cat']
    list_display_links = ['id', 'nome_cat']