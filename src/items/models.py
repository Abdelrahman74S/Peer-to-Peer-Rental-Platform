from django.contrib.gis.db import models
from django.conf import settings 
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.gis.geos import Point

# Create your models here.

EGYPT_CITIES = {
    'cairo': {'name': 'Cairo', 'coords': (31.2357, 30.0444)},
    'alexandria': {'name': 'Alexandria', 'coords': (29.9187, 31.2001)},
    'giza': {'name': 'Giza', 'coords': (31.2109, 29.9870)},
    'sharm': {'name': 'Sharm El-Sheikh', 'coords': (34.3299, 27.9158)},
    'hurghada': {'name': 'Hurghada', 'coords': (33.8116, 27.2579)},
    'luxor': {'name': 'Luxor', 'coords': (32.6396, 25.6872)},
    'aswan': {'name': 'Aswan', 'coords': (32.8998, 24.0889)},
    'mansoura': {'name': 'Mansoura', 'coords': (31.3805, 31.0409)},
    'tanta': {'name': 'Tanta', 'coords': (31.0019, 30.7865)},
    'port_said': {'name': 'Port Said', 'coords': (32.3019, 31.2653)},
    'suez': {'name': 'Suez', 'coords': (32.5498, 29.9668)},
    'ismailia': {'name': 'Ismailia', 'coords': (32.2715, 30.5965)},
    'zagazig': {'name': 'Zagazig', 'coords': (31.5046, 30.5765)},
    'damanhur': {'name': 'Damanhur', 'coords': (30.4682, 31.0341)},
    'minya': {'name': 'Minya', 'coords': (30.7503, 28.1099)},
    'assiut': {'name': 'Assiut', 'coords': (31.1837, 27.1809)},
    'sohag': {'name': 'Sohag', 'coords': (31.6948, 26.5490)},
    'qena': {'name': 'Qena', 'coords': (32.7160, 26.1551)},
    'banha': {'name': 'Banha', 'coords': (31.1792, 30.4659)},
    'kafr_sheikh': {'name': 'Kafr El-Sheikh', 'coords': (30.9381, 31.1063)},
}


CITY_CHOICES = [(key, value['name']) for key, value in EGYPT_CITIES.items()]


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True ,allow_unicode=True)
    description = models.TextField()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name,allow_unicode=True)
        super(Category, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True,allow_unicode=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE)
    
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    location = models.PointField(
        geography=True, 
        spatial_index=True,
        null=True, 
        blank=True,
    )    
    
    city = models.CharField(
        max_length=50, 
        choices=CITY_CHOICES,
        verbose_name="City"
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if self.city and not self.location:
            city_data = EGYPT_CITIES.get(self.city)
            if city_data:
                lng, lat = city_data['coords']
                self.location = Point(lng, lat, srid=4326)
        
        if not self.slug:
            self.slug = slugify(self.title,allow_unicode=True)
        super(Item, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.title

class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if self.is_primary:
            ItemImage.objects.filter(item=self.item, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Image for {self.item.title}"