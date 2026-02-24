from django.urls import path
from . import views

urlpatterns = [
    # ==================== CATEGORY URLS ====================
    path('categories/', views.ListCategoryView.as_view(), name='category_list'),
    path('categories/add/', views.CreateCategoryView.as_view(), name='category_create'),
    path('categories/<slug:slug>/', views.DetailCategoryView.as_view(), name='category_detail'),
    path('categories/<slug:slug>/edit/', views.UpdateCategoryView.as_view(), name='category_update'),
    path('categories/<slug:slug>/delete/', views.DeleteCategoryView.as_view(), name='category_delete'),

    # ==================== ITEM URLS ====================
    path('item_list/', views.ListItemView.as_view(), name='item_list'),
    path('item/add/', views.CreateItemView.as_view(), name='item_create'),
    path('item/<slug:slug>/', views.DetailItemView.as_view(), name='item_detail'),
    path('item/<slug:slug>/edit/', views.UpdateItemView.as_view(), name='item_update'),
    path('item/<slug:slug>/delete/', views.DeleteItemView.as_view(), name='item_delete'),

    # ==================== MY ITEMS & NEARBY URLS ====================
    path('my-items/', views.MyItemsView.as_view(), name='my_items'),
    path('my-pending-items/', views.MyPendingItemsView.as_view(), name='my_pending_items'),
    path('nearby/', views.MyNearbyItemsView.as_view(), name='my_nearby_items'),
]