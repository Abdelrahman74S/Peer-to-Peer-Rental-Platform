from django import forms
from .models import Item , Category , ItemImage
from mapwidgets.widgets import GooglePointFieldWidget

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  


class ItemForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultiFileInput(attrs={"multiple": True}),
        required=False,
    )
    class Meta:
        model = Item
        fields = ["title", "description", "price_per_day", "category", "slug", "location"]
        widgets = {
            'location': GooglePointFieldWidget,
        }
        
    def save(self, commit=True):
        instance = super().save(commit=commit)  
        if commit:
            self.save_images(instance) 
        return instance

    def save_images(self, instance): 
        images = self.files.getlist('images')
        for index, image in enumerate(images):
            is_primary = True if index == 0 and not instance.images.exists() else False
            ItemImage.objects.create(item=instance, image=image, is_primary=is_primary)
