from django.contrib import admin
from .models import Category, Item ,ItemImage
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    fields = ('image', 'is_primary')
    readonly_fields = ('created_at', 'updated_at')
    
@admin.register(Item)
class ItemAdmin(LeafletGeoAdmin): 
    list_display = ('title', 'category', 'owner', 'is_available', 'is_approved', 'created_at')
    list_filter = ('category', 'is_available', 'is_approved', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    inlines = [ItemImageInline]
