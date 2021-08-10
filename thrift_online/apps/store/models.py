from django.core.files import File
from django.db import models

from PIL import Image
from io import BytesIO

#function for making same size thumbnails keeping ratio and using white background
def resize(image_path, width, height):
    image_pil = Image.open(image_path)
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height

    if ratio_w < ratio_h:
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height

    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)

    return background.convert('RGB')


#functions for making separate media folders for products' images    
def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<category.slug>/product_<product.slug>
    if hasattr(instance, 'product'):
        return '{0}/product_{1}/{2}'.format(instance.product.category , instance.product.slug, filename)
    else:
        return '{0}/product_{1}/{2}'.format(instance.category, instance.slug, filename)


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)

    def __str__(self):
        return self.slug


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=5)
    date_added = models.DateTimeField(auto_now_add=True)
    num_available = models.IntegerField(default=1)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)

    image = models.ImageField(upload_to=product_directory_path, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=product_directory_path, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return ''

    def refine_image(self, image, size=(800, 600)):
        img = resize(image, size[0], size[1])

        thum_io = BytesIO()

        img.save(thum_io, 'JPEG')

        new_image = File(thum_io, name=self.image.name)
        return new_image
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = resize(image, size[0], size[1])

        thum_io = BytesIO()

        img.save(thum_io, 'JPEG')

        thumbnail = File(thum_io, name=image.name)
        return thumbnail

    def save(self, *args, **kwargs):
        if self.image:               # Check if we have already saved the image
            self.thumbnail = self.make_thumbnail(self.image)# (because of bugs)
            self.image = self.refine_image(self.image)

        super().save(*args, **kwargs)
    
    def super_save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to=product_directory_path, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=product_directory_path,blank=True, null=True)
    
    def __str__(self):
        return ('Снимка на ' + self.product.title)

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return ''
            
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return ''
    
    def refine_image(self, image,  size=(800, 600)):
        img = resize(image, size[0], size[1])

        thum_io = BytesIO()

        img.save(thum_io, 'JPEG')

        new_image = File(thum_io, name=self.image.name)
        return new_image
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = resize(image, size[0], size[1])

        thum_io = BytesIO()

        img.save(thum_io, 'JPEG')

        thumbnail = File(thum_io, name=image.name)
        return thumbnail

    def save(self, *args, **kwargs):
        if self.image:
            self.thumbnail = self.make_thumbnail(self.image)
            self.image = self.refine_image(self.image)

        super().save(*args, **kwargs)