import django
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.db.models import Prefetch , Q
from .models import EGYPT_CITIES, Item, Category , ItemImage
from .form import ItemForm, CategoryForm
from django.contrib.gis.db.models.functions import Distance
# Create your views here.


# ==================== CATEGORY VIEWS ====================
class CreateCategoryView(LoginRequiredMixin,UserPassesTestMixin ,CreateView):  
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')  
    
    def test_func(self):
        return self.request.user.is_staff

class ListCategoryView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

class UpdateCategoryView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')
    
    def test_func(self):
        return self.request.user.is_staff

class DeleteCategoryView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def test_func(self):
        return self.request.user.is_staff

class DetailCategoryView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'
    
# ==================== ITEM VIEWS ====================
class CreateItemView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Item'
        context['EGYPT_CITIES'] = EGYPT_CITIES  
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        with transaction.atomic():
            self.object = form.save()
            form.save_images(self.object)
            
        return super().form_valid(form)
    
class ListItemView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'
    paginate_by = 12  

    def get_queryset(self):
        queryset = Item.objects.filter(
            is_approved=True, 
            is_available=True
        ).prefetch_related(
            Prefetch('images', queryset=ItemImage.objects.order_by('-is_primary', '-created_at'))
        )

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(category__name__icontains=query)
            )

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        city_key = self.request.GET.get('city')
        if city_key:
            queryset = queryset.filter(city=city_key)

        price_range = self.request.GET.get('price')
        if price_range:
            try:
                if '-' in price_range:
                    min_p, max_p = price_range.split('-')
                    queryset = queryset.filter(price_per_day__gte=float(min_p), price_per_day__lte=float(max_p))
                elif price_range == '500+':
                    queryset = queryset.filter(price_per_day__gte=500.0)
            except (ValueError, TypeError):
                pass

        sort_by = self.request.GET.get('sort', '-created_at')
        
        allowed_sorts = ['price_per_day', '-price_per_day', 'created_at', '-created_at']
        if sort_by not in allowed_sorts:
            sort_by = '-created_at'
            
        return queryset.order_by(sort_by)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['EGYPT_CITIES'] = EGYPT_CITIES  
        context['categories'] = Category.objects.all()
        return context

class DetailItemView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'
    
    def get_queryset(self):
        return Item.objects.select_related(
            'category',           
            'owner'               
        ).prefetch_related(
            'images'              
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        
        context['similar_items'] = Item.objects.filter(
            category=item.category,
            is_approved=True,
            is_available=True
        ).exclude(
            id=item.id
        ).select_related('category', 'owner').prefetch_related('images')[:4]
        
        if item.location:
            user_location = self.request.user.profile.location if hasattr(self.request.user, 'profile') and self.request.user.profile.location else None
            
            if user_location:
                context['nearby_items'] = Item.objects.filter(
                    is_approved=True,
                    is_available=True,
                    location__distance_lte=(user_location, 10000)  # 10km
                ).exclude(
                    id=item.id
                ).annotate(
                    distance=Distance('location', user_location)
                ).order_by('distance').select_related('category', 'owner').prefetch_related('images')[:4]
        
        return context
    
class UpdateItemView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = '/item_list/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Item'
        context['EGYPT_CITIES'] = EGYPT_CITIES
        context['item'] = self.object 
        return context
    
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            new_images = self.request.FILES.getlist('images')
            if new_images:
                self.object.images.all().delete() 
                form.save_images(self.object)
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.owner or self.request.user.is_staff


class DeleteItemView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = '/item_list/'
    
    def test_func(self):
        item = self.get_object()
        return self.request.user == item.owner or self.request.user.is_staff

# ==================== MY ITEM VIEWS ====================

class MyItemsView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'items/my_items.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user , is_approved=True,).prefetch_related('images')

class MyPendingItemsView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'items/my_pending_items.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user , is_approved=False,).prefetch_related('images')

class MyNearbyItemsView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'items/my_nearby_items.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        user_location = self.request.user.profile.location
        return Item.objects.filter(
            is_approved=True, 
            is_available=True,
            location__distance_lte=(user_location, 5000)  
        ).annotate(
            distance=Distance('location', user_location)
        ).order_by('distance').prefetch_related('images')