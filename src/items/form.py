from django import forms
from .models import Item , Category , ItemImage
from leaflet.forms.widgets import LeafletWidget

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',  'description']

    
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  

class ItemForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultiFileInput(attrs={"multiple": True}),
        required=False,
        label="Item Images",
        help_text="Upload multiple images. First image will be set as primary."
    )
    
    class Meta:
        model = Item
        fields = ["title", "description", "price_per_day", "category", "city", "location", "is_available"]
        widgets = {
            'location': LeafletWidget(),  
        }
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].required = False
        self.fields['location'].widget.attrs.update({
            'class': 'leaflet-widget',
        })
        
    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        location = cleaned_data.get('location')
        
        if location:
            lat = location.y
            lng = location.x
            if not (22 <= lat <= 32 and 25 <= lng <= 35):
                self.add_error('location', 'Location must be within Egypt.')
        
        return cleaned_data
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            self.save_images(instance)
        return instance

    def save_images(self, instance): 
        images = self.files.getlist('images')
        for index, image in enumerate(images):
            is_primary = (index == 0 and not instance.images.exists())
            ItemImage.objects.create(
                item=instance, 
                image=image, 
                is_primary=is_primary
            )